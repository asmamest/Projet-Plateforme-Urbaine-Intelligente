"""
Modèles Spyne (types complexes SOAP)
"""
from spyne import ComplexModel, Unicode, Integer, Float, DateTime, Array

class Pollutant(ComplexModel):
    """Polluant individuel"""
    __namespace__ = "air.quality.service"
    
    nom = Unicode(min_occurs=1, doc="Nom du polluant (PM2.5, NO2, etc.)")
    valeur = Float(min_occurs=1, doc="Valeur mesurée")
    unite = Unicode(min_occurs=1, doc="Unité de mesure (µg/m³, ppm, etc.)")
    status = Unicode(min_occurs=1, doc="Statut (OK, MODERATE, ALERT)")
    timestamp = DateTime(min_occurs=1, doc="Horodatage de la mesure")

class PollutantList(ComplexModel):
    """Liste de polluants"""
    __namespace__ = "air.quality.service"
    
    zone = Unicode(min_occurs=1, doc="Code de la zone")
    pollutants = Array(Pollutant, doc="Liste des polluants")
    timestamp = DateTime(min_occurs=1, doc="Horodatage de la requête")

class AirQualityResult(ComplexModel):
    """Résultat de la qualité de l'air"""
    __namespace__ = "air.quality.service"
    
    zone = Unicode(min_occurs=1, doc="Code de la zone")
    aqi = Integer(min_occurs=1, doc="Indice AQI (0-500)")
    status = Unicode(min_occurs=1, doc="Statut (GOOD, MODERATE, UNHEALTHY, etc.)")
    description = Unicode(doc="Description textuelle")
    timestamp = DateTime(min_occurs=1, doc="Horodatage de la mesure")
    recommendations = Unicode(doc="Recommandations")

class ZoneComparison(ComplexModel):
    """Comparaison entre deux zones"""
    __namespace__ = "air.quality.service"
    
    zoneA = Unicode(min_occurs=1, doc="Code zone A")
    zoneB = Unicode(min_occurs=1, doc="Code zone B")
    aqi_A = Integer(min_occurs=1, doc="AQI zone A")
    aqi_B = Integer(min_occurs=1, doc="AQI zone B")
    cleaner_zone = Unicode(min_occurs=1, doc="Zone la plus propre")
    difference_aqi = Integer(doc="Différence d'AQI")
    recommendations = Unicode(doc="Recommandations")
    comparison_details = Unicode(doc="Détails de la comparaison")

class HistoricalDataPoint(ComplexModel):
    """Point de données historiques"""
    __namespace__ = "air.quality.service"
    
    timestamp = DateTime(min_occurs=1, doc="Horodatage")
    aqi = Integer(min_occurs=1, doc="Indice AQI")
    status = Unicode(min_occurs=1, doc="Statut")

class HistoricalSeries(ComplexModel):
    """Série temporelle historique"""
    __namespace__ = "air.quality.service"
    
    zone = Unicode(min_occurs=1, doc="Code de la zone")
    start_date = DateTime(min_occurs=1, doc="Date de début")
    end_date = DateTime(min_occurs=1, doc="Date de fin")
    granularity = Unicode(min_occurs=1, doc="Granularité (hourly, daily)")
    data_points = Array(HistoricalDataPoint, doc="Points de données")
    count = Integer(doc="Nombre de points")

class HealthStatus(ComplexModel):
    """État de santé du service"""
    __namespace__ = "air.quality.service"
    
    status = Unicode(min_occurs=1, doc="État (UP/DOWN)")
    version = Unicode(min_occurs=1, doc="Version du service")
    timestamp = DateTime(min_occurs=1, doc="Horodatage")
    database_status = Unicode(doc="État de la base de données")
    uptime_seconds = Integer(doc="Temps de fonctionnement en secondes")