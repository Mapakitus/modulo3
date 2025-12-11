"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from app.routers.web import artists, home, concerts
from app.routers.web import songs
from fastapi import APIRouter

router = APIRouter()

router.include_router(home.router)
router.include_router(songs.router)
router.include_router(artists.router)
router.include_router(concerts.router)