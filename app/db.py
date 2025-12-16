# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(
    settings.database_url,
    echo=True,  # показує SQL у консолі
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
