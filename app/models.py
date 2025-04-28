from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from .database import Base
from datetime import datetime

class License(Base):
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String, unique=True, index=True)
    owner_email = Column(String)
    is_active = Column(Boolean, default=True)
    max_devices = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=True)

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"))
    device_id = Column(String)
    app_version = Column(String)
    last_active = Column(DateTime, default=datetime.utcnow)

class BlockedVersion(Base):
    __tablename__ = "blocked_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True)
    reason = Column(String)
    blocked_at = Column(DateTime, default=datetime.utcnow)