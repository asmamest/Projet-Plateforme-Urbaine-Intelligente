"""
Repository pour l'accès aux données
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database.models import ZoneModel, AirQualityMeasurementModel, PollutantModel
import logging

logger = logging.getLogger("air-quality-soap")

class AirQualityRepository:
    """Repository pour les données de qualité de l'air"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_zone_by_code(self, code: str) -> Optional[ZoneModel]:
        """Récupère une zone par son code"""
        try:
            return self.db.query(ZoneModel).filter(ZoneModel.code == code.upper()).first()
        except Exception as e:
            logger.error(f"Erreur get_zone_by_code: {e}")
            return None
    
    def get_latest_measurement(self, zone_id: str) -> Optional[AirQualityMeasurementModel]:
        """Récupère la dernière mesure pour une zone"""
        try:
            return (
                self.db.query(AirQualityMeasurementModel)
                .filter(AirQualityMeasurementModel.zone_id == zone_id)
                .order_by(AirQualityMeasurementModel.timestamp.desc())
                .first()
            )
        except Exception as e:
            logger.error(f"Erreur get_latest_measurement: {e}")
            return None
    
    def get_pollutants_for_measurement(self, measurement_id: str) -> List[PollutantModel]:
        """Récupère tous les polluants pour une mesure"""
        try:
            return (
                self.db.query(PollutantModel)
                .filter(PollutantModel.measurement_id == measurement_id)
                .all()
            )
        except Exception as e:
            logger.error(f"Erreur get_pollutants: {e}")
            return []
    
    def get_pollutants_above_threshold(
        self, 
        measurement_id: str, 
        threshold: float
    ) -> List[PollutantModel]:
        """Récupère les polluants dépassant un seuil"""
        try:
            return (
                self.db.query(PollutantModel)
                .filter(
                    and_(
                        PollutantModel.measurement_id == measurement_id,
                        PollutantModel.valeur >= threshold
                    )
                )
                .all()
            )
        except Exception as e:
            logger.error(f"Erreur get_pollutants_above_threshold: {e}")
            return []
    
    def get_historical_data(
        self,
        zone_id: str,
        start_date: datetime,
        end_date: datetime,
        limit: int = 1000
    ) -> List[AirQualityMeasurementModel]:
        """Récupère les données historiques pour une période"""
        try:
            return (
                self.db.query(AirQualityMeasurementModel)
                .filter(
                    and_(
                        AirQualityMeasurementModel.zone_id == zone_id,
                        AirQualityMeasurementModel.timestamp >= start_date,
                        AirQualityMeasurementModel.timestamp <= end_date
                    )
                )
                .order_by(AirQualityMeasurementModel.timestamp.asc())
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Erreur get_historical_data: {e}")
            return []
        