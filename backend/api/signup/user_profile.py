from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, Annotated
from datetime import datetime

from api.utils import get_db_pool

router = APIRouter(prefix="/api/v1/users", tags=["User Profile"])

# =========================
# SCHEMAS
# =========================

class ProfileResponse(BaseModel):
    user_id: int
    first_name: Optional[
        Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    ]
    last_name: Optional[
        Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    ]
    email: EmailStr
    phone: Optional[
        Annotated[str, constr(strip_whitespace=True, min_length=10, max_length=15)]
    ]
    role: str
    created_at: Optional[datetime] = None


class ProfileUpdateRequest(BaseModel):
    first_name: Optional[
        Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    ] = Field(None)

    last_name: Optional[
        Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    ] = Field(None)

    email: Optional[EmailStr] = Field(None)

    phone: Optional[
        Annotated[str, constr(strip_whitespace=True, min_length=10, max_length=15)]
    ] = Field(None)

# =========================
# GET PROFILE
# =========================

@router.get("/me", response_model=ProfileResponse)
async def get_profile(request: Request):
    user = request.state.user
    user_id = int(user["sub"])

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, first_name, last_name, email, phone_number, role, created_at
            FROM siri.users
            WHERE id = $1
            """,
            user_id,
        )

    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": row["id"],
        "first_name": row["first_name"],
        "last_name": row["last_name"],
        "email": row["email"],
        "phone": row["phone_number"],
        "role": row["role"],
        "created_at": row["created_at"],
    }

# =========================
# UPDATE PROFILE
# =========================

@router.put("/me")
async def update_profile(request: Request, payload: ProfileUpdateRequest):
    user = request.state.user
    user_id = int(user["sub"])

    fields = payload.model_dump(exclude_unset=True)
    # Map API field to DB column
    if "phone" in fields:
        fields["phone_number"] = fields.pop("phone")

    if not fields:
        return {"message": "Nothing to update"}

    set_clause = ", ".join(f"{k} = ${i+2}" for i, k in enumerate(fields.keys()))
    values = list(fields.values())

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            f"""
            UPDATE siri.users
            SET {set_clause}
            WHERE id = $1
            """,
            user_id,
            *values,
        )

    return {"message": "Profile updated successfully"}