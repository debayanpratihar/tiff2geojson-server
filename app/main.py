from fastapi import FastAPI
from .database import engine, Base
from .routes import licenses, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TIFF2GeoJSON License Server",
    description="License management server for TIFF2GeoJSON software",
    version="1.0.0"
)

app.include_router(licenses.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1/admin")

@app.get("/")
def root():
    return {"message": "TIFF2GeoJSON License Server is running"}