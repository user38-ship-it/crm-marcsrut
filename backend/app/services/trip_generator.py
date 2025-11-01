from datetime import date, timedelta
from typing import Iterable, List

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.survey import Trip, TripTemplate

settings = get_settings()


class TripGeneratorService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _calculate_dates(self, start: date, occurrences: int, frequency: str) -> Iterable[date]:
        if frequency == "daily":
            delta = timedelta(days=1)
        elif frequency == "biweekly":
            delta = timedelta(days=14)
        else:
            delta = timedelta(days=7)

        current = start
        for _ in range(occurrences):
            yield current
            current += delta

    def create_trips(self, template: TripTemplate) -> List[Trip]:
        horizon = settings.trip_generation_horizon_days
        start_date = template.start_date
        occurrences = template.occurrences

        dates = list(self._calculate_dates(start_date, occurrences, template.frequency))
        dates = [d for d in dates if (d - start_date).days <= horizon]

        created_trips: List[Trip] = []
        for scheduled_date in dates:
            trip = Trip(template_id=template.id, scheduled_date=scheduled_date)
            self.session.add(trip)
            created_trips.append(trip)
        self.session.flush()
        return created_trips
