from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LicenseCreate(BaseModel):
    license_key: str
    owner_email: str
    max_devices: int = 1
    expiry_date: Optional[datetime] = None

class LicenseResponse(LicenseCreate):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class ActivationRequest(BaseModel):
    license_key: str
    device_id: str
    app_version: str

class ActivationResponse(BaseModel):
    token: str
    expiry: datetime
    status: str