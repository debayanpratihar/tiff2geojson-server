from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

def create_license(db: Session, license: schemas.LicenseCreate):
    db_license = models.License(
        license_key=license.license_key,
        owner_email=license.owner_email,
        max_devices=license.max_devices,
        expiry_date=license.expiry_date
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
        
    # Check if device is already registered
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
            
        # Register new device
        device = models.Device(
            license_id=license.id,
            device_id=request.device_id,
            app_version=request.app_version
        )
        db.add(device)
        db.commit()
    
    # Update last active time
    device.last_active = datetime.utcnow()
    db.commit()
    
    # Calculate expiry (30 days from now or license expiry)
    expiry = license.expiry_date or datetime.utcnow() + timedelta(days=30)
    
    return {
        "token": f"token_{license.id}_{device.id}",
        "expiry": expiry,
        "status": "activated"
    }

def check_blocked_version(db: Session, version: str):
    return db.query(models.BlockedVersion).filter(
        models.BlockedVersion.version == version
    ).first()