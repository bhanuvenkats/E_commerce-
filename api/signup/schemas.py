from pydantic import BaseModel, EmailStr, HttpUrl, constr, validator, root_validator, model_validator, Field
from typing import Optional, Dict, Annotated
import re
from datetime import datetime

class AddressBase(BaseModel):
    address_line1: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=255)]
    city: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    postal_code: Optional[Annotated[str, constr(strip_whitespace=True, max_length=20)]] = None
    country: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]
    address_type: Annotated[str, constr(strip_whitespace=True, to_lower=True)] = Field(..., pattern="^(home|work|other)$")
    is_default: Optional[bool] = False

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    address_line1: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=255)]]
    city: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]]
    postal_code: Optional[Annotated[str, constr(strip_whitespace=True, max_length=20)]]
    country: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]]
    address_type: Optional[Annotated[str, constr(strip_whitespace=True, to_lower=True)]] = Field(None, pattern="^(home|work|other)$")
    is_default: Optional[bool]

class AddressResponse(BaseModel):
    id: int
    address_line1: str
    city: str
    postal_code: Optional[str]
    country: str
    address_type: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

class SignupRequest(BaseModel):
    first_name: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]] = Field(None, description="User's first name")
    last_name: Optional[Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]] = Field(None, description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    username: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=50)] = Field(..., description="Desired username")
    password: Annotated[str, constr(min_length=8)] = Field(..., description="User's password (must be strong)")
    phone_number: Optional[str] = Field(
        None, description="Optional phone number in E.164 format (e.g., +1234567890)"
    )
    role: Optional[str] = Field("customer", description="User role (default: customer)")

    @validator("phone_number")
    def validate_phone(cls, v):
        if v is not None:
            # E.164 format: +[country][number], e.g., +1234567890
            if not re.fullmatch(r"\+[1-9]\d{1,14}", v):
                raise ValueError("Invalid E.164 phone number format")
        return v

class SignupResponse(BaseModel):
    user_id: int
    message: str

class ErrorResponse(BaseModel):
    error: str
    fields: Optional[Dict[str, str]] = None

class SendOTPRequest(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    @model_validator(mode="after")
    def check_email_or_phone(self):
        if not self.email and not self.phone_number:
            raise ValueError('One of email or phone_number must be provided')
        return self

# =========================
# PYDANTIC SCHEMAS  ✅ MUST BE BEFORE ROUTES
# =========================

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordVerify(BaseModel):
    email: EmailStr

    otp: Annotated[
        str,
        constr(min_length=4, max_length=4, pattern="^[0-9]{4}$")
    ]

    new_password: Annotated[
        str,
        constr(min_length=8)
    ]

    # ✅ ONLY FIELD ADDED
    confirm_password: Annotated[
        str,
        constr(min_length=8)
    ]


class ForgotPasswordResponse(BaseModel):
    message: str

