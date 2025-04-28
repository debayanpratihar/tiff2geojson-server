from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta

def create_license(db: Session, license: schemas.LicenseCreate):
    db_license = models.License(
        license_key=license.license_key,
        owner_email=license.owner_email,
        max_devices=license.max_devices
    )
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

def activate_license(db: Session, request: schemas.ActivationRequest):
    license = db.query(models.License).filter(
        models.License.license_key == request.license_key,
        models.License.is_active == True
    ).first()
    
    if not license:
        return None
        
    # Check if device exists
    device = db.query(models.Device).filter(
        models.Device.license_id == license.id,
        models.Device.device_id == request.device_id
    ).first()
    
    if not device:
        # Check device limit
        device_count = db.query(models.Device).filter(
            models.Device.license_id == license.id
        ).count()
        
        if device_count >= license.max_devices:
            return None
            
        device = models.Device(
            license_id=license.id,
            device_id=request.device_id,
            app_version=request.app_version
        )
        db.add(device)
    
    device.last_active = datetime.utcnow()
    db.commit()
    
    return {
        "token": f"valid_{license.id}_{device.id}",
        "expiry": license.expiry_date,
        "status": "active"
    }

def block_version(db: Session, version: str, reason: str):
    existing = db.query(models.BlockedVersion).filter(
        models.BlockedVersion.version == version
    ).first()
    
    if existing:
        return False
        
    blocked = models.BlockedVersion(
        version=version,
        reason=reason
    )
    db.add(blocked)
    db.commit()
    return True