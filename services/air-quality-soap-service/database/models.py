"""
Modèles SQLAlchemy pour la base de données
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.connection import Base

class ZoneModel(Base):
    """Table des zones géographiques (partagée avec REST)"""
    __tablename__ = "zones"
    
    id = Column(String(36), primary_key=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    type_zone = Column(String(50), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relations
    measurements = relationship("AirQualityMeasurementModel", back_populates="zone", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Zone {self.code}: {self.nom}>"

class AirQualityMeasurementModel(Base):
    """Table des mesures de qualité de l'air"""
    __tablename__ = "air_quality_measurements"
    
    id = Column(String(36), primary_key=True)
    zone_id = Column(String(36), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False, index=True)
    aqi = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    zone = relationship("ZoneModel", back_populates="measurements")
    pollutants = relationship("PollutantModel", back_populates="measurement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Measurement AQI={self.aqi} Zone={self.zone_id}>"

class PollutantModel(Base):
    """Table des polluants"""
    __tablename__ = "pollutants"
    
    id = Column(String(36), primary_key=True)
    measurement_id = Column(String(36), ForeignKey("air_quality_measurements.id", ondelete="CASCADE"), nullable=False, index=True)
    nom = Column(String(50), nullable=False)
    valeur = Column(Float, nullable=False)
    unite = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relation
    measurement = relationship("AirQualityMeasurementModel", back_populates="pollutants")
    
    def __repr__(self):
        return f"<Pollutant {self.nom}={self.valeur}{self.unite}>"

        