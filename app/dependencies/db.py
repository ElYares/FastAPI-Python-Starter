from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Base para modelos ORM
Base = declarative_base()

# SQLite necesita check_same_thread=False si usas sesiones en FastAPI
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DB_ECHO,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

def get_db():
    """
    Dependency de FastApi para obtener una sesion de DB por request
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()