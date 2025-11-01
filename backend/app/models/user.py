from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    phone: str = Column(String(32), unique=True, index=True, nullable=False)
    full_name: str | None = Column(String(255), nullable=True)
    company_name: str | None = Column(String(255), nullable=True)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    routes: List["SurveyRoute"] = relationship("SurveyRoute", back_populates="user")
    trip_templates: List["TripTemplate"] = relationship(
        "TripTemplate", back_populates="user"
    )
