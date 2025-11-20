from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import create_engine, Integer, String, Float, Boolean, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session


    

        


#aplicación FastAPI

#Crea la instancia de la aplicación FastAPI
app = FastAPI(title="Cancioncitas API", version="1.0.0")

#endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Welcome to the Cancioncitas API!"}

#ENDPOINTS CRUD

# GET - obtener TODAS las canciones
@app.get("/api/songs", response_model=list[SongResponse])
def find_all(db: Session = Depends(get_db)):
    #db.execute(): para ejecutar la consulta
    #select(Song): crea consulta SELECT * FROM songs
    #.scalars(): extrae los objetos Song de la consulta
    #.all(): convierte los objetos en una lista
    return db.execute(select(Song)).scalars().all()

# GET - obtener UNA canción por ID
@app.get("/api/songs/{id}", response_model=SongResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    #buscar canción por id de la ruta con un select y devuelve el objeto 
    # o None si no existe
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado la canción con id {id}"
        )
    return song

# POST - crear una canción
@app.post("/api/songs", response_model=SongResponse, status_code=status.HTTP_201_CREATED)

def create(song_dto: SongCreate, db: Session = Depends(get_db)):
    
    #crear objeto Song a partir del DTO
    song = Song(
        title=song_dto.title,
        artist=song_dto.artist,
        duration_seconds=song_dto.duration_seconds,
        explicit=song_dto.explicit
    )
    
    #agrega el objeto a la sesión
    db.add(song)
    #guarda el objeto en la base de datos
    db.commit()
    #refresca el objeto para obtener el id generado
    db.refresh(song)
    #devuelve el objeto creado
    return song

# PUT - actualizar COMPLETAMENTE una canción
@app.put("/api/songs/{id}", response_model=SongResponse)
def update_all(id: int, song_dto: SongUpdate, db: Session = Depends(get_db)):
    #buscar canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado la canción con id {id}"
        )
    """
    #actualizar campos
    song.title = song_dto.title
    song.artist = song_dto.artist
    song.duration_seconds = song_dto.duration_seconds
    song.explicit = song_dto.explicit
    """
    #actualizar campos de forma dinámica
    # guardar los datos del DTO en un diccionario
    update_data = song_dto.model_dump()
    #Bucle para asignar cada campo al objeto song
    for field, value in update_data.items():
        #usar setattr para asignar el valor al campo correspondiente
        setattr(song, field, value)
    
    #guardar cambios en la base de datos
    db.commit()
    #refrescar objeto
    db.refresh(song)
    return song

# PATCH - actualizar PARCIALMENTE una canción
@app.patch("/api/songs/{id}", response_model=SongResponse)
def update_partial(id: int, song_dto: SongPatch, db: Session = Depends(get_db)):
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado la canción con id {id}"
        )
  
    update_data = song_dto.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(song, field, value)
    
    db.commit() # confirma los cambios en base datos
    db.refresh(song) # refresca el objeto
    return song

# DELETE - eliminar una canción
@app.delete("/api/songs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    #eliminar canción
    db.delete(song)
    db.commit()
    return None