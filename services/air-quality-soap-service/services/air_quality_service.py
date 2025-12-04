"""
Implémentation du service SOAP - Logique métier
"""
from spyne import Application, rpc, ServiceBase, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from models.air_quality_models import (
    AirQualityResult, PollutantList, Pollutant, ZoneComparison,
    HistoricalSeries, HistoricalDataPoint, HealthStatus
)
from repositories.data_repository import AirQualityRepository
from database.connection import get_db
from datetime import datetime
import logging
import time

logger = logging.getLogger("air-quality-soap")

# Temps de démarrage pour le uptime
START_TIME = time.time()

class AirQualityService(ServiceBase):
    """Service SOAP pour la qualité de l'air"""
    
    @rpc(Unicode, _returns=AirQualityResult)
    def GetAQI(ctx, zone):
        """
        Récupère l'indice AQI pour une zone donnée
        
        Args:
            zone: Code de la zone (ex: CENTRE, NORD, SUD, EST)
            
        Returns:
            AirQualityResult avec AQI et informations
        """
        logger.info(f"GetAQI appelé pour zone: {zone}")
        
        if not zone or zone.strip() == "":
            raise Fault("Client", "Le code de zone ne peut pas être vide")
        
        db = next(get_db())
        try:
            repo = AirQualityRepository(db)
            
            # Récupérer la zone
            zone_obj = repo.get_zone_by_code(zone)
            if not zone_obj:
                raise Fault("Client", f"Zone '{zone}' introuvable")
            
            # Récupérer la dernière mesure
            measurement = repo.get_latest_measurement(zone_obj.id)
            if not measurement:
                raise Fault("Server", f"Aucune mesure disponible pour la zone '{zone}'")
            
            # Déterminer les recommandations
            recommendations = _get_recommendations(measurement.aqi)
            description = _get_aqi_description(measurement.aqi)
            
            result = AirQualityResult(
                zone=zone.upper(),
                aqi=measurement.aqi,
                status=measurement.status,
                description=description,
                timestamp=measurement.timestamp,
                recommendations=recommendations
            )
            
            logger.info(f"GetAQI réussi pour {zone}: AQI={measurement.aqi}")
            return result
            
        except Fault:
            raise
        except Exception as e:
            logger.error(f"Erreur GetAQI: {e}")
            raise Fault("Server", f"Erreur interne: {str(e)}")
        finally:
            db.close()
    
    @rpc(Unicode, _returns=PollutantList)
    def GetPollutants(ctx, zone):
        """
        Récupère les niveaux de polluants pour une zone
        
        Args:
            zone: Code de la zone
            
        Returns:
            PollutantList avec tous les polluants mesurés
        """
        logger.info(f"GetPollutants appelé pour zone: {zone}")
        
        if not zone or zone.strip() == "":
            raise Fault("Client", "Le code de zone ne peut pas être vide")
        
        db = next(get_db())
        try:
            repo = AirQualityRepository(db)
            
            zone_obj = repo.get_zone_by_code(zone)
            if not zone_obj:
                raise Fault("Client", f"Zone '{zone}' introuvable")
            
            measurement = repo.get_latest_measurement(zone_obj.id)
            if not measurement:
                raise Fault("Server", f"Aucune mesure disponible pour la zone '{zone}'")
            
            pollutants_db = repo.get_pollutants_for_measurement(measurement.id)
            
            pollutants = [
                Pollutant(
                    nom=p.nom,
                    valeur=p.valeur,
                    unite=p.unite,
                    status=p.status,
                    timestamp=measurement.timestamp
                )
                for p in pollutants_db
            ]
            
            result = PollutantList(
                zone=zone.upper(),
                pollutants=pollutants,
                timestamp=datetime.now()
            )
            
            logger.info(f"GetPollutants réussi pour {zone}: {len(pollutants)} polluants")
            return result
            
        except Fault:
            raise
        except Exception as e:
            logger.error(f"Erreur GetPollutants: {e}")
            raise Fault("Server", f"Erreur interne: {str(e)}")
        finally:
            db.close()
    
    @rpc(Unicode, Unicode, _returns=ZoneComparison)
    def CompareZones(ctx, zoneA, zoneB):
        """
        Compare la qualité de l'air entre deux zones
        
        Args:
            zoneA: Code de la première zone
            zoneB: Code de la deuxième zone
            
        Returns:
            ZoneComparison avec analyse comparative
        """
        logger.info(f"CompareZones appelé: {zoneA} vs {zoneB}")
        
        if not zoneA or not zoneB:
            raise Fault("Client", "Les codes de zone ne peuvent pas être vides")
        
        if zoneA.upper() == zoneB.upper():
            raise Fault("Client", "Les deux zones doivent être différentes")
        
        db = next(get_db())
        try:
            repo = AirQualityRepository(db)
            
            # Zone A
            zone_obj_a = repo.get_zone_by_code(zoneA)
            if not zone_obj_a:
                raise Fault("Client", f"Zone '{zoneA}' introuvable")
            
            measurement_a = repo.get_latest_measurement(zone_obj_a.id)
            if not measurement_a:
                raise Fault("Server", f"Aucune mesure pour la zone '{zoneA}'")
            
            # Zone B
            zone_obj_b = repo.get_zone_by_code(zoneB)
            if not zone_obj_b:
                raise Fault("Client", f"Zone '{zoneB}' introuvable")
            
            measurement_b = repo.get_latest_measurement(zone_obj_b.id)
            if not measurement_b:
                raise Fault("Server", f"Aucune mesure pour la zone '{zoneB}'")
            
            # Comparaison
            cleaner = zoneA.upper() if measurement_a.aqi < measurement_b.aqi else zoneB.upper()
            diff = abs(measurement_a.aqi - measurement_b.aqi)
            
            # Détails de comparaison
            details = _build_comparison_details(
                zone_obj_a.nom, measurement_a,
                zone_obj_b.nom, measurement_b
            )
            
            recommendations = _build_comparison_recommendations(
                measurement_a.aqi, measurement_b.aqi, cleaner
            )
            
            result = ZoneComparison(
                zoneA=zoneA.upper(),
                zoneB=zoneB.upper(),
                aqi_A=measurement_a.aqi,
                aqi_B=measurement_b.aqi,
                cleaner_zone=cleaner,
                difference_aqi=diff,
                recommendations=recommendations,
                comparison_details=details
            )
            
            logger.info(f"CompareZones réussi: {cleaner} est plus propre (diff={diff})")
            return result
            
        except Fault:
            raise
        except Exception as e:
            logger.error(f"Erreur CompareZones: {e}")
            raise Fault("Server", f"Erreur interne: {str(e)}")
        finally:
            db.close()
    
    @rpc(Unicode, DateTime, DateTime, Unicode, _returns=HistoricalSeries)
    def GetHistory(ctx, zone, startDate, endDate, granularity):
        """
        Récupère l'historique des mesures pour une période
        
        Args:
            zone: Code de la zone
            startDate: Date de début
            endDate: Date de fin
            granularity: Granularité (hourly, daily)
            
        Returns:
            HistoricalSeries avec les données temporelles
        """
        logger.info(f"GetHistory appelé: {zone}, {startDate} à {endDate}, {granularity}")
        
        if not zone:
            raise Fault("Client", "Le code de zone ne peut pas être vide")
        
        if not startDate or not endDate:
            raise Fault("Client", "Les dates de début et fin sont obligatoires")
        
        if startDate >= endDate:
            raise Fault("Client", "La date de début doit être antérieure à la date de fin")
        
        if granularity not in ['hourly', 'daily']:
            raise Fault("Client", "Granularité invalide. Valeurs acceptées: hourly, daily")
        
        db = next(get_db())
        try:
            repo = AirQualityRepository(db)
            
            zone_obj = repo.get_zone_by_code(zone)
            if not zone_obj:
                raise Fault("Client", f"Zone '{zone}' introuvable")
            
            # Limite de 1000 points
            measurements = repo.get_historical_data(
                zone_obj.id, startDate, endDate, limit=1000
            )
            
            if not measurements:
                raise Fault("Server", f"Aucune donnée historique pour la période demandée")
            
            data_points = [
                HistoricalDataPoint(
                    timestamp=m.timestamp,
                    aqi=m.aqi,
                    status=m.status
                )
                for m in measurements
            ]
            
            result = HistoricalSeries(
                zone=zone.upper(),
                start_date=startDate,
                end_date=endDate,
                granularity=granularity,
                data_points=data_points,
                count=len(data_points)
            )
            
            logger.info(f"GetHistory réussi: {len(data_points)} points retournés")
            return result
            
        except Fault:
            raise
        except Exception as e:
            logger.error(f"Erreur GetHistory: {e}")
            raise Fault("Server", f"Erreur interne: {str(e)}")
        finally:
            db.close()
    
    @rpc(Unicode, Float, _returns=PollutantList)
    def FilterPollutants(ctx, zone, threshold):
        """
        Filtre les polluants dépassant un seuil
        
        Args:
            zone: Code de la zone
            threshold: Seuil minimal de valeur
            
        Returns:
            PollutantList avec polluants filtré """
            
    
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