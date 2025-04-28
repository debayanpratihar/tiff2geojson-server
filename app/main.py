from fastapi import FastAPI, Depends
from .database import SessionLocal
from .routes import licenses, admin

app = FastAPI()

# Include routers
app.include_router(licenses.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "TIFF2GeoJSON License Server"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()