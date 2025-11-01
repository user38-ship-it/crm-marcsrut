from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    phone: str = Field(..., regex=r"^\+?[0-9]{10,15}$")


class RegisterResponse(BaseModel):
    phone: str
    otp_code: str
    message: str = "OTP sent"


class VerifyRequest(BaseModel):
    phone: str = Field(..., regex=r"^\+?[0-9]{10,15}$")
    code: str = Field(..., min_length=4, max_length=6)
    full_name: Optional[str] = None
    company_name: Optional[str] = None


class UserProfile(BaseModel):
    id: int
    phone: str
    full_name: Optional[str]
    company_name: Optional[str]
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True
