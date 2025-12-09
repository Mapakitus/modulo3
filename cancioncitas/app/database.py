"""
Configuración de la base de datos
"""



# crear motor de conexión a base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine(
    "sqlite:///cancioncitas.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# clase base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass

# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()


# INICIALIZACIÓN BASE DE DATOS

# método inicializar con canciones por defecto
def init_db():
    """
    Inicializa la base de datos con canciones por defecto si está vacía.
    Sólo crea las canciones si no existen ya en la base de datos.
    """
    from app.models import Song, Artist
    from datetime import datetime
    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import sessionmaker, DeclarativeBase

    from app.models.concert import Concert, ConcertStatus
    
    # crear todas las tablas
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        existing_songs = db.execute(select(Song)).scalars().all()
        
        if existing_songs:
            return
        
        default_artists = [
            Artist(name="ABBA", birth_date=datetime(1972, 1, 1)),
            Artist(name="Amaral", birth_date=datetime(1972, 8, 4)),
            Artist(name="Ludwig van Beethoven", birth_date=None),
            Artist(name="Joan Manuel Serrat", birth_date=None),
            Artist(name="Darren Korb", birth_date=None),
            Artist(name="Michael Jackson", birth_date=None),
            Artist(name="Nirvana", birth_date=None)
        ]
        
        db.add_all(default_artists)
        db.commit()
        
        #obtener los artistas para tener sus ids
        artists = db.execute(select(Artist)).scalars().all()
        artist_dict = {artist.name: artist.id for artist in artists}
        
        # refresca los artistas para obtener su id
        for artist in default_artists:
            db.refresh(artist)
        
        default_songs = [
            Song(title="Mamma Mia", artist="ABBA", duration_seconds=300, explicit=False),
            Song(title="Sin ti no soy nada", artist="Amaral", duration_seconds=250, explicit=False),
            Song(title="Sonata para piano nº 14", artist="Ludwig van Beethoven", duration_seconds=800, explicit=False),
            Song(title="Mediterráneo", artist="Joan Manuel Serrat", duration_seconds=400, explicit=False),
            Song(title="Never to Return", artist="Darren Korb", duration_seconds=300, explicit=False),
            Song(title="Billie Jean", artist="Michael Jackson", duration_seconds=294, explicit=False),
            Song(title="Smells Like Teen Spirit", artist="Nirvana", duration_seconds=301, explicit=True)
        ]
        
        # agregar las canciones
        db.add_all(default_songs)
        db.commit()
        
        default_concerts = [
            Concert(
                name="ABBA - Primera gira",
                price=85.00,
                capacity=50000,
                status=ConcertStatus.SCHEDULED,
                is_sold_out=False,
                date_time=(2026, 6, 15, 20, 0),
                img_url="https://placehold.co/600x400?text=ABBA+Primera+Gira",
                artist_id=artist_dict.get("ABBA")
            ),
            Concert(
                name="Amaral - Hacia lo salvaje",
                price=5.00,
                capacity=500000,
                status=ConcertStatus.SCHEDULED,
                is_sold_out=False,
                date_time=(2026, 10, 12, 17, 30),
                img_url="https://placehold.co/600x400?text=Amaral+Concierto",
                artist_id=artist_dict.get("Amaral")
            ),
             Concert(
                name="Metallica - Master of Puppets",
                price=50.00,
                capacity=200000,
                status=ConcertStatus.COMPLETED,
                is_sold_out=True,
                date_time=(2026, 10, 12, 17, 30),
                img_url="https://placehold.co/600x400?text=Amaral+Concierto",
                artist_id=artist_dict.get("Metallica")
            ),
            Concert(
                name="Muse - Supermassive black hole",
                price=150.00,
                capacity=3400000,
                status=ConcertStatus.CANCELLED,
                is_sold_out=False,
                date_time=(2026, 11, 11, 21, 30),
                img_url="https://placehold.co/600x400?text=Muse+Concert",
                artist_id=artist_dict.get("Muse")
            ),
            
        ]
        
        
    finally:
        db.close()