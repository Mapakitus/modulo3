"""
Rutas de la web para la página de inicio
Renderiza un HTML
"""


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

#configurar jinja2
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
   
