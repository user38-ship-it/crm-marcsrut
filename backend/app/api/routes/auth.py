from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    UserProfile,
    VerifyRequest,
)
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
def register_user(
    payload: RegisterRequest, session: Session = Depends(get_session)
) -> RegisterResponse:
    user = auth_service.create_or_update_user(session, payload.phone)
    otp = auth_service.create_otp(session, payload.phone)
    session.commit()

    return RegisterResponse(phone=user.phone, otp_code=otp.code)


@router.post("/verify", response_model=UserProfile)
def verify_user(
    payload: VerifyRequest, session: Session = Depends(get_session)
) -> UserProfile:
    is_valid = auth_service.verify_otp(session, payload.phone, payload.code)
    if not is_valid:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP code",
        )

    user = auth_service.create_or_update_user(session, payload.phone)
    user.full_name = payload.full_name
    user.company_name = payload.company_name
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserProfile.from_orm(user)
