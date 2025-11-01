from datetime import datetime, timedelta
import random

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.otp import OTPCode
from app.models.user import User

settings = get_settings()


def generate_otp_code(length: int = 5) -> str:
    return "".join(random.choices("0123456789", k=length))


def create_or_update_user(session: Session, phone: str) -> User:
    user = session.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        user = User(phone=phone)
        session.add(user)
        session.flush()
    return user


def create_otp(session: Session, phone: str) -> OTPCode:
    code = generate_otp_code()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiration_minutes)

    otp = OTPCode(phone=phone, code=code, expires_at=expires_at, is_used=False)
    session.add(otp)
    session.flush()
    return otp


def verify_otp(session: Session, phone: str, code: str) -> bool:
    otp = (
        session.execute(
            select(OTPCode)
            .where(OTPCode.phone == phone)
            .where(OTPCode.code == code)
            .order_by(OTPCode.created_at.desc())
        )
        .scalars()
        .first()
    )
    if not otp:
        return False
    if otp.is_used or otp.expires_at < datetime.utcnow():
        return False

    session.execute(
        update(OTPCode).where(OTPCode.id == otp.id).values(is_used=True)
    )
    return True
