from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, security

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])
security_scheme = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    token = credentials.credentials
    payload = security.verify_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return payload

@router.post("/licenses", response_model=schemas.LicenseResponse)
def create_license(
    license: schemas.LicenseCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    return crud.create_license(db, license)

@router.post("/block-version")
def block_version(
    version: str,
    reason: str,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    blocked = crud.block_version(db, version, reason)
    return {"status": "blocked" if blocked else "already blocked"}