from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="backend/app/web/templates")

router = APIRouter()


def render_template(template_name: str, request: Request, page_title: str, active_page: str):
    return templates.TemplateResponse(
        template_name,
        {
            "request": request,
            "page_title": page_title,
            "active_page": active_page,
        },
    )


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return render_template("dashboard.html", request, "Панель", "dashboard")


@router.get("/trips", response_class=HTMLResponse)
async def trips(request: Request):
    return render_template("trips.html", request, "Рейси", "trips")


@router.get("/drivers", response_class=HTMLResponse)
async def drivers(request: Request):
    return render_template("drivers.html", request, "Водії", "drivers")


@router.get("/bookings", response_class=HTMLResponse)
async def bookings(request: Request):
    return render_template("bookings.html", request, "Бронювання", "bookings")


@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    return render_template("analytics.html", request, "Аналітика", "analytics")


@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    return render_template("settings.html", request, "Налаштування", "settings")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return render_template("login.html", request, "Вхід", "login")
