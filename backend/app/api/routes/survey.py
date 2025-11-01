from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models.survey import SurveyRoute, TripTemplate
from app.models.user import User
from app.schemas.survey import (
    SurveyRoutesRequest,
    SurveyRoutesResponse,
)
from app.services.trip_generator import TripGeneratorService

router = APIRouter(prefix="/survey", tags=["survey"])


@router.post("/routes", response_model=SurveyRoutesResponse)
def create_survey_routes(
    payload: SurveyRoutesRequest, session: Session = Depends(get_session)
) -> SurveyRoutesResponse:
    user = session.execute(select(User).where(User.phone == payload.phone)).scalar_one_or_none()
    if not user or not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not verified",
        )

    created_routes: list[SurveyRoute] = []
    created_templates: list[TripTemplate] = []
    generator = TripGeneratorService(session)

    for route_input in payload.routes:
        route = SurveyRoute(
            user_id=user.id,
            origin=route_input.origin,
            destination=route_input.destination,
            departure_time=route_input.departure_time,
            return_time=route_input.return_time,
            frequency=route_input.frequency,
            driver_count=payload.driver_count,
        )
        session.add(route)
        session.flush()
        created_routes.append(route)

        template = TripTemplate(
            user_id=user.id,
            survey_route_id=route.id,
            start_date=route_input.start_date,
            occurrences=route_input.occurrences,
            frequency=route_input.frequency,
            capacity=route_input.capacity or 0,
        )
        session.add(template)
        session.flush()
        generator.create_trips(template)
        session.refresh(template)
        created_templates.append(template)

    session.commit()

    for route in created_routes:
        session.refresh(route)
    for template in created_templates:
        session.refresh(template)

    return SurveyRoutesResponse(routes=created_routes, templates=created_templates)
