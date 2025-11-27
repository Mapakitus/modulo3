"""
Configuración de la aplicación FastAPI
"""
from fastapi import FastAPI
from app.database import init_db
from app.routers.api import router as api_router
from app.routers.web import router as web_router



#Crea la instancia de la aplicación FastAPI
app = FastAPI(title="Cancioncitas API", version="1.0.0")

#inicializa la base de datos con canciones por defecto
init_db()

#incluir routers de la API
app.include_router(api_router)
app.include_router(web_router)

"""
# endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la app Cancioncitas"}
"""