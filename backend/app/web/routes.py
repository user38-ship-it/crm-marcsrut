from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="backend/app/web/templates")
router = APIRouter()


def _template_response(request: Request, template_name: str, context: dict | None = None) -> HTMLResponse:
    data = {"request": request, "current_path": request.url.path}
    if context:
        data.update(context)
    return templates.TemplateResponse(template_name, data)


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    stats = {
        "trips": 12,
        "occupancy": "78%",
        "drivers": 5,
    }
    return _template_response(request, "dashboard.html", {"stats": stats, "page_title": "Головна"})


@router.get("/trips", response_class=HTMLResponse)
def trips(request: Request) -> HTMLResponse:
    return _template_response(request, "trips.html", {"page_title": "Рейси"})


@router.get("/drivers", response_class=HTMLResponse)
def drivers(request: Request) -> HTMLResponse:
    return _template_response(request, "drivers.html", {"page_title": "Водії"})


@router.get("/bookings", response_class=HTMLResponse)
def bookings(request: Request) -> HTMLResponse:
    return _template_response(request, "bookings.html", {"page_title": "Бронювання"})


@router.get("/analytics", response_class=HTMLResponse)
def analytics(request: Request) -> HTMLResponse:
    return _template_response(request, "analytics.html", {"page_title": "Аналітика"})


@router.get("/settings", response_class=HTMLResponse)
def settings(request: Request) -> HTMLResponse:
    return _template_response(request, "settings.html", {"page_title": "Налаштування"})


@router.get("/login", response_class=HTMLResponse)
def login(request: Request) -> HTMLResponse:
    return _template_response(request, "login.html", {"page_title": "Вхід"})
