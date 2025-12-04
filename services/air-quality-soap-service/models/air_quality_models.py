"""
Modèles de données pour le service SOAP Air Quality
"""
from spyne import ComplexModel, Unicode, Integer, Float, DateTime, Array


class Pollutant(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    name = Unicode(min_occurs=1, max_occurs=1)
    value = Float(min_occurs=1, max_occurs=1)
    unit = Unicode(min_occurs=1, max_occurs=1)
    timestamp = DateTime(min_occurs=1, max_occurs=1)
    status = Unicode(min_occurs=1, max_occurs=1)


class AirQualityResult(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    zone = Unicode(min_occurs=1, max_occurs=1)
    aqi = Integer(min_occurs=1, max_occurs=1)
    category = Unicode(min_occurs=1, max_occurs=1)
    timestamp = DateTime(min_occurs=1, max_occurs=1)
    description = Unicode(min_occurs=1, max_occurs=1)


class PollutantList(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    zone = Unicode(min_occurs=1, max_occurs=1)
    pollutants = Array(Pollutant, min_occurs=0)
    timestamp = DateTime(min_occurs=1, max_occurs=1)


class ZoneComparison(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    zoneA = Unicode(min_occurs=1, max_occurs=1)
    zoneB = Unicode(min_occurs=1, max_occurs=1)
    aqiA = Integer(min_occurs=1, max_occurs=1)
    aqiB = Integer(min_occurs=1, max_occurs=1)
    cleanest_zone = Unicode(min_occurs=1, max_occurs=1)
    difference = Integer(min_occurs=1, max_occurs=1)
    recommendations = Unicode(min_occurs=1, max_occurs=1)
    timestamp = DateTime(min_occurs=1, max_occurs=1)


class DataPoint(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    timestamp = DateTime(min_occurs=1, max_occurs=1)
    aqi = Integer(min_occurs=1, max_occurs=1)
    pm25 = Float(min_occurs=0, max_occurs=1)
    pm10 = Float(min_occurs=0, max_occurs=1)
    no2 = Float(min_occurs=0, max_occurs=1)
    co2 = Float(min_occurs=0, max_occurs=1)
    o3 = Float(min_occurs=0, max_occurs=1)
    so2 = Float(min_occurs=0, max_occurs=1)


class HistoricalSeries(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    zone = Unicode(min_occurs=1, max_occurs=1)
    start_date = DateTime(min_occurs=1, max_occurs=1)
    end_date = DateTime(min_occurs=1, max_occurs=1)
    granularity = Unicode(min_occurs=1, max_occurs=1)
    data_points = Array(DataPoint, min_occurs=0)


class HealthStatus(ComplexModel):
    __namespace__ = 'http://smartcity.air-quality.soap/models'
    status = Unicode(min_occurs=1, max_occurs=1)
    version = Unicode(min_occurs=1, max_occurs=1)
    uptime_seconds = Integer(min_occurs=1, max_occurs=1)
    database_status = Unicode(min_occurs=1, max_occurs=1)
    last_check = DateTime(min_occurs=1, max_occurs=1)