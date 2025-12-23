# =========================
# IMPORTS
# =========================
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, EmailStr, constr
from typing_extensions import Annotated
from datetime import datetime, timedelta, timezone
import random
import logging
import os
from api.signup.schemas import (
    ForgotPasswordRequest,
    ForgotPasswordVerify,
    ForgotPasswordResponse
)

from twilio.rest import Client
from dotenv import load_dotenv

from api.utils import (
    get_db_pool,
    hash_password,
    is_password_strong,
    passwords_match
)

# =========================
# CONFIG
# =========================
router = APIRouter(prefix="/api/v1", tags=["ForgotPassword"])
logging.basicConfig(level=logging.INFO)
OTP_EXPIRY_MINUTES = 10
load_dotenv()


# =========================
# HELPERS
# =========================

def generate_otp():
    return f"{random.randint(1000, 9999):04d}"


async def send_sms(phone_number: str, otp: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        raise RuntimeError("Twilio credentials are not set")

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=from_number,
        to=phone_number
    )


# =========================
# REQUEST OTP
# =========================

@router.post(
    "/forgot-password/request",
    response_model=ForgotPasswordResponse
)
async def forgot_password_request(
    payload: ForgotPasswordRequest = Body(...)
):
    pool = await get_db_pool()
    async with pool.acquire() as conn:

        user = await conn.fetchrow(
            "SELECT id, phone_number FROM siri.users WHERE email = $1",
            payload.email
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user["phone_number"]:
            raise HTTPException(
                status_code=400,
                detail="No phone number registered"
            )

        otp = generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=OTP_EXPIRY_MINUTES
        )

        await conn.execute(
            """
            INSERT INTO siri.password_reset_otps
            (user_id, otp_code, expires_at, is_used, created_at)
            VALUES ($1, $2, $3, false, NOW())
            """,
            user["id"], otp, expires_at
        )

        await send_sms(user["phone_number"], otp)

        return ForgotPasswordResponse(
            message="OTP sent to your registered phone number."
        )


# =========================
# VERIFY OTP & RESET PASSWORD
# =========================

@router.post(
    "/forgot-password/verify",
    response_model=ForgotPasswordResponse
)
async def forgot_password_verify(
    payload: ForgotPasswordVerify = Body(...)
):
    pool = await get_db_pool()
    async with pool.acquire() as conn:

        user = await conn.fetchrow(
            "SELECT id, password_hash FROM siri.users WHERE email = $1",
            payload.email
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp_row = await conn.fetchrow(
            """
            SELECT id, expires_at, is_used
            FROM siri.password_reset_otps
            WHERE user_id = $1 AND otp_code = $2
            ORDER BY created_at DESC
            LIMIT 1
            """,
            user["id"], payload.otp
        )

        if not otp_row:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        if otp_row["is_used"]:
            raise HTTPException(status_code=400, detail="OTP already used")
        if otp_row["expires_at"] < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="OTP expired")

        if not is_password_strong(payload.new_password):
            raise HTTPException(
                status_code=400,
                detail="Password is not strong enough"
            )

        if not passwords_match(
            payload.new_password,
            payload.confirm_password
        ):
            raise HTTPException(
                status_code=400,
                detail="Passwords do not match"
            )

        new_hash = hash_password(payload.new_password)
        if new_hash == user["password_hash"]:
            raise HTTPException(
                status_code=400,
                detail="New password cannot be same as old password"
            )

        await conn.execute(
            """
            UPDATE siri.users
            SET password_hash = $1, updated_at = NOW()
            WHERE id = $2
            """,
            new_hash, user["id"]
        )

        await conn.execute(
            """
            UPDATE siri.password_reset_otps
            SET is_used = true
            WHERE id = $1
            """,
            otp_row["id"]
        )

        return ForgotPasswordResponse(
            message="Password has been reset successfully."
        )