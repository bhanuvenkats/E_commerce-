from fastapi import APIRouter, status, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict
from dotenv import load_dotenv
import asyncpg
import logging
import os
import re

from api.utils import get_db_pool, hash_password, is_password_strong

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

router = APIRouter(prefix="/api/v1", tags=["Signup"])


# ======================================================
# ===================== SCHEMAS =========================
# ======================================================

class SignupRequest(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: EmailStr
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8)
    phone_number: Optional[str] = Field(
        None, description="10-digit Indian mobile number"
    )
    role: Optional[str] = Field("customer")

    @validator("phone_number", pre=True)
    def normalize_and_validate_phone(cls, v):
        if v is None:
            return v

        # Auto add +91 for Indian numbers
        if re.fullmatch(r"\d{10}", v):
            return "+91" + v

        # Accept valid E.164 numbers
        if re.fullmatch(r"\+[1-9]\d{1,14}", v):
            return v

        raise ValueError("Invalid phone number format")


class SignupResponse(BaseModel):
    user_id: int
    message: str


class ErrorResponse(BaseModel):
    error: str
    fields: Optional[Dict[str, str]] = None


# ======================================================
# ================= DB HELPERS ==========================
# ======================================================

async def is_email_or_username_taken(conn, email, username):
    row = await conn.fetchrow(
        "SELECT 1 FROM siri.users WHERE email = $1 OR username = $2",
        email, username
    )
    return row is not None


async def create_user(conn, user_data):
    row = await conn.fetchrow(
        """
        INSERT INTO siri.users
        (username, email, password_hash, first_name, last_name, phone_number,
         is_active, role, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, true, $7, NOW(), NOW())
        RETURNING id
        """,
        user_data["username"],
        user_data["email"],
        user_data["password_hash"],
        user_data["first_name"],
        user_data["last_name"],
        user_data["phone_number"],
        user_data["role"]
    )
    return row["id"] if row else None


# ======================================================
# ==================== ROUTE ============================
# ======================================================

@router.post(
    "/signup",
    response_model=SignupResponse,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
async def signup(
    request: Request,
    payload: SignupRequest = Body(
        ...,
        example={
            "first_name": "Bhanu Venkat",
            "last_name": "Srikakulapu",
            "email": "bhanuvenkatsrikakulapu8@gmail.com",
            "username": "bhanuvenkat",
            "password": "Nagaraju454@",
            "phone_number": "9392495546"
        }
    )
):
    logging.info(f"[signup] Incoming request: {payload}")

    # Password strength validation
    if not is_password_strong(payload.password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Validation failed",
                "fields": {"password": "Password is not secure enough"}
            }
        )

    pool = await get_db_pool()
    async with pool.acquire() as conn:

        # Check duplicate email / username
        if await is_email_or_username_taken(conn, payload.email, payload.username):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": "Username or email already exists"}
            )

        password_hash = hash_password(payload.password)

        user_data = {
            "username": payload.username,
            "email": payload.email,
            "password_hash": password_hash,
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "phone_number": payload.phone_number,  # already +91 normalized
            "role": payload.role or "customer"
        }

        try:
            created_id = await create_user(conn, user_data)
        except asyncpg.exceptions.UniqueViolation:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": "Username or email already exists"}
            )
        except Exception as e:
            logging.error(f"[signup] DB error: {e}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"error": "Service temporarily unavailable. Please try again later."}
            )

        return SignupResponse(
            user_id=created_id,
            message="User registered."
        )