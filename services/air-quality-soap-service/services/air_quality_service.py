"""
Service métier Air Quality
"""
import time
from datetime import datetime, timedelta
from spyne import Fault

from models.air_quality_models import (
    AirQualityResult, PollutantList, ZoneComparison,
    HistoricalSeries, HealthStatus, Pollutant, DataPoint
)
from repositories.data_repository import DataRepository
from utils.logger import setup_logger

logger = setup_logger('service', 'logs/service.log')

START_TIME = time.time()
SERVICE_VERSION = "1.0.0"


class AirQualityServiceImpl:
    
    def __init__(self):
        self.repository = DataRepository()
        logger.info("Service Air Quality initialisé")
    
    def get_aqi(self, zone: str) -> AirQualityResult:
        if not zone or zone.strip() == "":
            raise Fault(faultcode="Client", faultstring="Zone vide")
        
        try:
            data = self.repository.get_current_data(zone)
            if not data:
                raise Fault(faultcode="Server", faultstring=f"Zone '{zone}' introuvable")
            
            aqi = data.get('aqi', 0)
            category = self._get_aqi_category(aqi)
            
            result = AirQualityResult()
            result.zone = zone
            result.aqi = aqi
            result.category = category
            result.timestamp = datetime.now()
            result.description = self._get_aqi_description(category)
            
            return result
        except Fault:
            raise
        except Exception as e:
            logger.error(f"Erreur get_aqi: {str(e)}")
            raise Fault(faultcode="Server", faultstring=str(e))
    
    def get_pollutants(self, zone: str) -> PollutantList:
        if not zone or zone.strip() == "":
            raise Fault(faultcode="Client", faultstring="Zone vide")
        
        try:
            data = self.repository.get_current_data(zone)
            if not data:
                raise Fault(faultcode="Server", faultstring=f"Zone '{zone}' introuvable")
            
            timestamp = datetime.now()
            pollutants = []
            
            for name, key in [('PM2.5', 'pm25'), ('PM10', 'pm10'), 
                             ('NO2', 'no2'), ('CO2', 'co2'), 
                             ('O3', 'o3'), ('SO2', 'so2')]:
                if key in data:
                    p = Pollutant()
                    p.name = name
                    p.value = data[key]
                    p.unit = self._get_unit(key)
                    p.timestamp = timestamp
                    p.status = self._get_pollutant_status(data[key], key)
                    pollutants.append(p)
            
            result = PollutantList()
            result.zone = zone
            result.pollutants = pollutants
            result.timestamp = timestamp
            
            return result
        except Fault:
            raise
        except Exception as e:
            raise Fault(faultcode="Server", faultstring=str(e))
    
    def compare_zones(self, zoneA: str, zoneB: str) -> ZoneComparison:
        if not zoneA or not zoneB:
            raise Fault(faultcode="Client", faultstring="Zones vides")
        
        try:
            dataA = self.repository.get_current_data(zoneA)
            dataB = self.repository.get_current_data(zoneB)
            
            if not dataA:
                raise Fault(faultcode="Server", faultstring=f"Zone '{zoneA}' introuvable")
            if not dataB:
                raise Fault(faultcode="Server", faultstring=f"Zone '{zoneB}' introuvable")
            
            aqiA = dataA.get('aqi', 0)
            aqiB = dataB.get('aqi', 0)
            
            result = ZoneComparison()
            result.zoneA = zoneA
            result.zoneB = zoneB
            result.aqiA = aqiA
            result.aqiB = aqiB
            result.cleanest_zone = zoneA if aqiA < aqiB else zoneB
            result.difference = abs(aqiA - aqiB)
            result.recommendations = self._get_recommendations(aqiA, aqiB, zoneA, zoneB)
            result.timestamp = datetime.now()
            
            return result
        except Fault:
            raise
        except Exception as e:
            raise Fault(faultcode="Server", faultstring=str(e))
    
    def get_history(self, zone: str, start_date, end_date, granularity: str) -> HistoricalSeries:
        if not zone:
            raise Fault(faultcode="Client", faultstring="Zone vide")
        if granularity not in ['hourly', 'daily']:
            raise Fault(faultcode="Client", faultstring="Granularité invalide (hourly/daily)")
        if start_date >= end_date:
            raise Fault(faultcode="Client", faultstring="Date de début >= date de fin")
        
        try:
            history = self.repository.get_historical_data(zone, start_date, end_date, granularity)
            
            data_points = []
            for entry in history:
                dp = DataPoint()
                dp.timestamp = entry['timestamp']
                dp.aqi = entry.get('aqi', 0)
                dp.pm25 = entry.get('pm25')
                dp.pm10 = entry.get('pm10')
                dp.no2 = entry.get('no2')
                dp.co2 = entry.get('co2')
                dp.o3 = entry.get('o3')
                dp.so2 = entry.get('so2')
                data_points.append(dp)
            
            result = HistoricalSeries()
            result.zone = zone
            result.start_date = start_date
            result.end_date = end_date
            result.granularity = granularity
            result.data_points = data_points
            
            return result
        except Fault:
            raise
        except Exception as e:
            raise Fault(faultcode="Server", faultstring=str(e))
    
    def filter_pollutants(self, zone: str, threshold: float) -> PollutantList:
        if not zone:
            raise Fault(faultcode="Client", faultstring="Zone vide")
        if threshold < 0:
            raise Fault(faultcode="Client", faultstring="Seuil négatif")
        
        try:
            all_pollutants = self.get_pollutants(zone)
            filtered = [p for p in all_pollutants.pollutants if p.value > threshold]
            
            result = PollutantList()
            result.zone = zone
            result.pollutants = filtered
            result.timestamp = datetime.now()
            
            return result
        except Fault:
            raise
        except Exception as e:
            raise Fault(faultcode="Server", faultstring=str(e))
    
    def health_check(self) -> HealthStatus:
        try:
            db_status = "UP" if self.repository.check_health() else "DOWN"
            
            result = HealthStatus()
            result.status = "UP" if db_status == "UP" else "DEGRADED"
            result.version = SERVICE_VERSION
            result.uptime_seconds = int(time.time() - START_TIME)
            result.database_status = db_status
            result.last_check = datetime.now()
            
            return result
        except Exception as e:
            logger.error(f"Erreur health_check: {str(e)}")
            raise Fault(faultcode="Server", faultstring=str(e))
    
    def _get_aqi_category(self, aqi: int) -> str:
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    def _get_aqi_description(self, category: str) -> str:
        descriptions = {
            "Good": "La qualité de l'air est satisfaisante",
            "Moderate": "Qualité acceptable pour la plupart",
            "Unhealthy for Sensitive Groups": "Risque pour personnes sensibles",
            "Unhealthy": "Risque pour toute la population",
            "Very Unhealthy": "Avertissement de santé",
            "Hazardous": "Alerte sanitaire"
        }
        return descriptions.get(category, "Inconnu")
    
    def _get_pollutant_status(self, value: float, pollutant_type: str) -> str:
        thresholds = {
            'pm25': 35.0, 'pm10': 50.0, 'no2': 100.0,
            'co2': 1000.0, 'o3': 70.0, 'so2': 75.0
        }
        threshold = thresholds.get(pollutant_type, 50.0)
        
        if value <= threshold:
            return "OK"
        elif value <= threshold * 1.5:
            return "ALERT"
        else:
            return "CRITICAL"
    
    def _get_unit(self, pollutant: str) -> str:
        units = {
            'pm25': 'µg/m³', 'pm10': 'µg/m³',
            'no2': 'ppb', 'co2': 'ppm',
            'o3': 'ppb', 'so2': 'ppb'
        }
        return units.get(pollutant, 'unit')
    
    def _get_recommendations(self, aqiA: int, aqiB: int, zoneA: str, zoneB: str) -> str:
        diff = abs(aqiA - aqiB)
        better = zoneA if aqiA < aqiB else zoneB
        
        if diff < 20:
            return f"Différence mineure. Les deux zones ont une qualité similaire."
        elif diff < 50:
            return f"Préférez {better} pour activités extérieures."
        else:
            return f"Différence significative. Privilégiez fortement {better}."