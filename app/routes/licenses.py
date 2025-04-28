from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/api/v1/licenses", tags=["licenses"])

@router.post("/activate", response_model=schemas.ActivationResponse)
def activate_license(request: schemas.ActivationRequest, db: Session = Depends(get_db)):
    result = crud.activate_license(db, request)
    if not result:
        raise HTTPException(status_code=400, detail="Activation failed")
    return result

@router.get("/status")
def check_version_status(version: str, db: Session = Depends(get_db)):
    blocked = crud.check_blocked_version(db, version)
    return {"blocked": bool(blocked), "reason": blocked.reason if blocked else None}