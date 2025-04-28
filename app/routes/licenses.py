from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud
from .dependencies import get_db

router = APIRouter(prefix="/licenses", tags=["licenses"])

@router.post("/activate", response_model=schemas.ActivationResponse)
def activate_license(
    request: schemas.ActivationRequest,
    db: Session = Depends(get_db)
):
    result = crud.activate_license(db, request)
    if not result:
        raise HTTPException(status_code=400, detail="Activation failed")
    return result

@router.get("/check-version")
def check_version(version: str, db: Session = Depends(get_db)):
    blocked = db.query(models.BlockedVersion).filter(
        models.BlockedVersion.version == version
    ).first()
    return {"blocked": bool(blocked), "reason": blocked.reason if blocked else None}