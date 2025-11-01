from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class SurveyRouteInput(BaseModel):
    origin: str
    destination: str
    departure_time: time
    return_time: Optional[time] = None
    frequency: str = Field(default="weekly", regex=r"^(daily|weekly|biweekly)$")
    start_date: date
    occurrences: int = Field(default=4, ge=1, le=30)
    capacity: Optional[int] = Field(default=0, ge=0)

    @validator("frequency")
    def normalize_frequency(cls, value: str) -> str:
        return value.lower()


class SurveyRoutesRequest(BaseModel):
    phone: str = Field(..., regex=r"^\+?[0-9]{10,15}$")
    driver_count: int = Field(default=1, ge=1)
    routes: List[SurveyRouteInput]


class SurveyRouteResponse(BaseModel):
    id: int
    origin: str
    destination: str
    departure_time: time
    return_time: Optional[time]
    frequency: str
    driver_count: int

    class Config:
        orm_mode = True


class TripResponse(BaseModel):
    id: int
    scheduled_date: date
    status: str

    class Config:
        orm_mode = True


class TripTemplateResponse(BaseModel):
    id: int
    start_date: date
    frequency: str
    occurrences: int
    capacity: int
    trips: List[TripResponse]

    class Config:
        orm_mode = True


class SurveyRoutesResponse(BaseModel):
    routes: List[SurveyRouteResponse]
    templates: List[TripTemplateResponse]
