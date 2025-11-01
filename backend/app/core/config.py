from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field(default="Booking CRM")
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@postgres:5432/booking"
    )
    redis_url: str = Field(default="redis://redis:6379/0")

    otp_expiration_minutes: int = Field(default=10)
    trip_generation_horizon_days: int = Field(default=14)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
