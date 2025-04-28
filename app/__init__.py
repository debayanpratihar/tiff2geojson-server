from fastapi import FastAPI
from .database import engine, Base

def create_app():
    app = FastAPI(title="TIFF2GeoJSON License Server",
                 description="License management server for TIFF2GeoJSON software",
                 version="1.0.0")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    return app