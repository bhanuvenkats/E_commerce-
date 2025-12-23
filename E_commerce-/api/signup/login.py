from fastapi import APIRouter, status, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from api.utils import get_db_pool, DB_SCHEMA, hash_password
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone
import uuid
import logging
from pydantic import BaseModel, EmailStr
from typing import Optional

# Load environment variables from project root .env
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

router = APIRouter(prefix="/api/v1", tags=["Login"])

logging.basicConfig(level=logging.INFO)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

"""
POST /api/v1/login
Request JSON body:
{
  "email": "alice@example.com",
  "password": "SuperSecretPass!2024"
}
Both email and password are required.
"""

@router.post("/login", responses={
    200: {"description": "JWT token issued."},
    400: {"description": "Validation failed"},
    401: {"description": "Invalid credentials or MFA not verified"},
    503: {"description": "Service temporarily unavailable. Please try again later."},
})
async def login(
    request: Request,
    payload: LoginRequest = Body(
        ..., 
        example={
            "email": "bhanuvenkatsrikakulapu8@gmail.com",
            "password": "Nagaraju454@"
        }
    )
):
    logging.info(f"Received login request: {payload}")
    password = payload.password
    email = payload.email
    if not password or not email:
        logging.warning(f"Missing credentials: password={password}, email={email}")
        return JSONResponse(status_code=400, content={"error": "Validation failed", "fields": {"credentials": "Provide both email and password"}})
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # 1. Lookup user by email only
        logging.info(f"Looking up user by email: {email}")
        user = await conn.fetchrow(f"SELECT * FROM {DB_SCHEMA}.users WHERE email = $1", email)
        logging.info(f"User lookup result: {user}")
        if not user:
            logging.warning("User not found or invalid credentials.")
            return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
        # 2. Check password
        logging.info("Checking password hash...")
        if user["password_hash"] != hash_password(password):
            logging.warning("Password hash does not match.")
            return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
        # 3. Issue JWT with device and permissions
        try:
            now_aware = datetime.now(timezone.utc)
            now = now_aware.replace(tzinfo=None)
            exp = (now_aware + timedelta(minutes=JWT_EXPIRE_MINUTES)).replace(tzinfo=None)
            device = {"type": "browser", "os": "linux"}  # Mocked device info
            permissions = {}
            jwt_payload = {
                "sub": str(user["id"]),
                "iat": int(now_aware.timestamp()),
                "exp": int((now_aware + timedelta(minutes=JWT_EXPIRE_MINUTES)).timestamp()),
                "device": device,
                "permissions": permissions
            }
            logging.info(f"Creating JWT with payload: {jwt_payload}")
            token = jwt.encode(jwt_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            logging.info(f"JWT created successfully.")
        except Exception as e:
            logging.error(f"Error creating JWT: {e}")
            return JSONResponse(status_code=503, content={"error": "Service temporarily unavailable. Please try again later."})
        # Stateless JWT authentication: do not create or update session records
        logging.info(f"Login successful for user_id={user['id']}")
        user_profile = {
            "user_id": user["id"],
            "username": user.get("username"),
            "email": user.get("email"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "phone_number": user.get("phone_number"),
            "is_active": user.get("is_active"),
            "role": user.get("role"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
        }
        return {
            "token": token,
            "expires_at": exp.isoformat(),
            "profile": user_profile
        }
