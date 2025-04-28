from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import schemas, crud
from .dependencies import get_db, validate_admin_token

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBearer()

@router.post("/licenses", response_model=schemas.License)
def create_license(
    license: schemas.LicenseCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if not validate_admin_token(credentials.credentials):
        raise HTTPException(status_code=403, detail="Invalid admin token")
    
    return crud.create_license(db, license)

@router.post("/block-version")
def block_version(
    request: schemas.BlockVersionRequest,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if not validate_admin_token(credentials.credentials):
        raise HTTPException(status_code=403, detail="Invalid admin token")
    
    if crud.block_version(db, request.version, request.reason):
        return {"status": "version blocked"}
    return {"status": "version already blocked"}