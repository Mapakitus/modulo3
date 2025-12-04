from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Artist

# configuración de Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# router para rutas web
router = APIRouter(prefix="/artists", tags=["web"])

# listar artistas
@router.get("", response_class=HTMLResponse)
def list_artists(request: Request, db: Session = Depends(get_db)):
    artists = db.execute(select(Artist)).scalars().all()
    
    return templates.TemplateResponse(
        "artists/list.html",
        {"request": request, "artists": artists}
    )
    
# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "artists/form.html",
        {"request": request, "artist": None}
    )

# crear nuevo artista
@router.post("/new", response_class=HTMLResponse)
def create_artist(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(None), #opcional
    db: Session = Depends(get_db)
):
    errors = []
    
    # convertir birth_date de DD/MM/YYYY a datetime
    birth_date_value = None
    if birth_date and birth_date.strip():
        try:
            birth_date_value = datetime.strptime(birth_date, "%d/%m/%Y")
        except ValueError:
            errors.append("La fecha de nacimiento no tiene un formato válido (DD/MM/YYYY)")
            
    form_data = {
        "name": name,
        # Si ya se convirtió correctamente, lo mostramos en el formulario en el mismo formato
        "birth_date": birth_date_value.strftime("%d/%m/%Y") if birth_date_value else birth_date
    }
    
    # validar campos obligatorios
    if not name or not name.strip():
        errors.append("El nombre es obligatorio")
        
    # si hay errores, mostrar el formulario con los errores
    if errors:
        return templates.TemplateResponse(
            "artists/form.html",
            {"request": request, "artist": None, "errors": errors, "form_data": form_data}
        )
    
    # crear artista
    try:
        artist = Artist(
            name=name.strip(),
            birth_date=birth_date_value       
        )
        db.add(artist)
        db.commit()
        db.refresh(artist)
        
        # redirigir a pantalla detalle
        return RedirectResponse(url=f"/artists/{artist.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el artista: {str(e)}")
        return templates.TemplateResponse(
            "artists/form.html",
            {"request": request, "artist": None, "errors": errors, "form_data": form_data}
        )
    
# detalle artista (http://localhost:8000/artists/5)
@router.get("/{artist_id}", response_class=HTMLResponse)
def artist_detail(request: Request, artist_id: int, db: Session = Depends(get_db)):
    artist = db.execute(select(Artist).where(Artist.id == artist_id)).scalar_one_or_none()
    
    if artist is None:
        raise HTTPException(status_code=404, detail="404 - Artista no encontrad@")
    
    return templates.TemplateResponse(
        "artists/detail.html",
        {"request": request, "artist": artist}
    )
    
# mostrar formulario editar
@router.get("/{artist_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, artist_id: int, db: Session = Depends(get_db)):
    # obtener artista por id
    artist = db.execute(select(Artist).where(Artist.id == artist_id)).scalar_one_or_none()
    
    # lanzar error 404 si no existe canción
    if artist is None:
        raise HTTPException(status_code=404, detail="404 - Artista  no encontrado")
    
    return templates.TemplateResponse(
        "artists/form.html",
        {"request": request, "artist": artist}
    )

# editar artista existente
@router.post("/{artist_id}/edit", response_class=HTMLResponse)
def update_artist(
    request: Request,
    artist_id: int,
    name: str = Form(...),
    birth_date: str = Form(None), #opcional
    db: Session = Depends(get_db)
):
    artist = db.execute(select(Artist).where(Artist.id == artist_id)).scalar_one_or_none()
    
    if artist is None:
        raise HTTPException(status_code=404, detail="404 - Artista no encontrado")
    
    errors = []

    # convertir birth_date de DD/MM/YYYY a datetime
    birth_date_value = None
    if birth_date and birth_date.strip():
        try:
            birth_date_value = datetime.strptime(birth_date, "%d/%m/%Y")
        except ValueError:
            errors.append("La fecha de nacimiento no tiene un formato válido (DD/MM/YYYY)")
            
    form_data = {
        "name": name,
        # Si ya se convirtió correctamente, lo mostramos en el formulario en el mismo formato
        "birth_date": birth_date_value.strftime("%d/%m/%Y") if birth_date_value else birth_date
    }
    
    # validar campos obligatorios
    if not name or not name.strip():
        errors.append("El nombre es obligatorio")
        
    # si hay errores, mostrar el formulario con los errores
    if errors:
        return templates.TemplateResponse(
            "artists/form.html",
            {"request": request, "artist": None, "errors": errors, "form_data": form_data}
        )
    
    # editar artista
    try:
        artist.name=name.strip()
        artist.birth_date=birth_date_value       
        
        
        db.commit()
        db.refresh(artist)
        
        # redirigir a pantalla detalle
        return RedirectResponse(url=f"/artists/{artist.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar el artista: {str(e)}")
        return templates.TemplateResponse(
            "artists/form.html",
            {"request": request, "artist": artist, "errors": errors, "form_data": form_data}
        )