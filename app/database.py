from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Try multiple environment variable names for flexibility
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")

if not DATABASE_URL:
    # Fallback for local development
    DATABASE_URL = "postgresql://user:password@localhost/tiff2geojson"
    print("Warning: Using default local database URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()