"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""
from app.routers.api import songs
from app.routers.api import concerts
from fastapi import APIRouter


#Router principal
router = APIRouter()

#incluir router de songs en router principal
router.include_router(songs.router)
#incluir router de concerts en router principal
router.include_router(concerts.router)