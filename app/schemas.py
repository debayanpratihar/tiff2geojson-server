from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LicenseBase(BaseModel):
    license_key: str
    owner_email: str
    max_devices: Optional[int] = 1

class LicenseCreate(LicenseBase):
    pass

class License(LicenseBase):
    id: int
    is_active: bool
    created_at: datetime
    expiry_date: datetime
    
    class Config:
        orm_mode = True

class DeviceBase(BaseModel):
    device_id: str
    app_version: str

class ActivationRequest(DeviceBase):
    license_key: str

class ActivationResponse(BaseModel):
    token: str
    expiry: datetime
    status: str

class BlockVersionRequest(BaseModel):
    version: str
    reason: str