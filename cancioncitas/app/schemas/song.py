"""
Esquemas Pydantic para estructura y validación de datos de canciones
"""

from pydantic import BaseModel, ConfigDict, field_validator


#modelos pydantic (schemas)
class SongResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    artist: str
    duration_seconds: int | None
    explicit: bool | None

#modelo para crear canciones (POST)
class SongCreate(BaseModel):
    title: str
    artist: str
    duration_seconds: int | None = None
    explicit: bool | None = None
    
    @field_validator('title', 'artist')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        #verifica que el campo no esté vacío o contenga solo espacios en blanco
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío o contener solo espacios en blanco.')
        #retorna el valor sin espacios en blanco delante y detrás (normalizar)
        return v.strip()
    
    @field_validator('duration_seconds')
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        #valida que la duración no sea None ni negativa
        if v is not None and v < 0:
            raise ValueError('La duración de la canción no puede ser negativa.')
        
        return v

    
#modelo para actualizar canciones (PUT)
#Todos los campos son obligatorios
class SongUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str 
    artist: str
    duration_seconds: int | None 
    explicit: bool | None
    
    @field_validator('title', 'artist')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        #verifica que el campo no esté vacío o contenga solo espacios en blanco
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío o contener solo espacios en blanco.')
        #retorna el valor sin espacios en blanco delante y detrás (normalizar)
        return v.strip() 
    
    @field_validator('duration_seconds')
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        #valida que la duración no sea None ni negativa
        if v is not None and v < 0:
            raise ValueError('La duración de la canción no puede ser negativa.')
        
        return v
    
#modelo para actualizar canciones parcialmente (PATCH)
#solo se envían los campos a modificar
class SongPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    artist: str | None = None
    duration_seconds: int | None = None
    explicit: bool | None = None
    
    @field_validator('title', 'artist')
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        #Si no se proporciona valor (None), no hacer validación
        if v is None:
            return None
        
        # Si se proporciona valor, verificar que no esté vacío o contenga solo espacios en blanco
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío o contener solo espacios en blanco.')
            
        #retorna el valor sin espacios en blanco delante y detrás (normalizar)
        return v.strip()
    
    @field_validator('duration_seconds')
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        #valida que la duración no sea negativa
        if v < 0:
            raise ValueError('La duración de la canción no puede ser negativa.')
        
        return v