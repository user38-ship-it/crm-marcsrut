from datetime import datetime, time
from typing import List

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.base import Base


class SurveyRoute(Base):
    __tablename__ = "survey_routes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    departure_time = Column(Time, nullable=False)
    return_time = Column(Time, nullable=True)
    driver_count = Column(Integer, nullable=False, default=1)
    frequency = Column(String(32), nullable=False, default="weekly")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="routes")
    trip_templates: List["TripTemplate"] = relationship(
        "TripTemplate", back_populates="survey_route"
    )


class TripTemplate(Base):
    __tablename__ = "trip_templates"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    survey_route_id = Column(Integer, ForeignKey("survey_routes.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    occurrences = Column(Integer, nullable=False, default=4)
    frequency = Column(String(32), nullable=False, default="weekly")
    capacity = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="trip_templates")
    survey_route = relationship("SurveyRoute", back_populates="trip_templates")
    trips: List["Trip"] = relationship("Trip", back_populates="template")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("trip_templates.id"), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    status = Column(String(32), nullable=False, default="scheduled")

    template = relationship("TripTemplate", back_populates="trips")
