"""
Tests unitaires pour AirQualityService
"""
import pytest
from datetime import datetime, timedelta
from spyne import Fault

from services.air_quality_service import AirQualityServiceImpl


class TestAirQualityService:
    
    @pytest.fixture
    def service(self):
        return AirQualityServiceImpl()
    
    def test_get_aqi_success(self, service):
        result = service.get_aqi('downtown')
        assert result is not None
        assert result.zone == 'downtown'
        assert result.aqi > 0
        assert result.category in ['Good', 'Moderate', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
        assert result.timestamp is not None
    
    def test_get_aqi_invalid_zone(self, service):
        with pytest.raises(Fault) as exc:
            service.get_aqi('nonexistent_zone')
        assert 'introuvable' in str(exc.value.faultstring)
    
    def test_get_aqi_empty_zone(self, service):
        with pytest.raises(Fault) as exc:
            service.get_aqi('')
        assert 'vide' in str(exc.value.faultstring)
    
    def test_get_pollutants_success(self, service):
        result = service.get_pollutants('downtown')
        assert result is not None
        assert result.zone == 'downtown'
        assert len(result.pollutants) > 0
        
        for pollutant in result.pollutants:
            assert pollutant.name in ['PM2.5', 'PM10', 'NO2', 'CO2', 'O3', 'SO2']
            assert pollutant.value >= 0
            assert pollutant.status in ['OK', 'ALERT', 'CRITICAL']
    
    def test_compare_zones_success(self, service):
        result = service.compare_zones('park', 'industrial')
        assert result is not None
        assert result.zoneA == 'park'
        assert result.zoneB == 'industrial'
        assert result.aqiA > 0
        assert result.aqiB > 0
        assert result.cleanest_zone in ['park', 'industrial']
        assert result.difference >= 0
        assert len(result.recommendations) > 0
    
    def test_compare_zones_same(self, service):
        result = service.compare_zones('downtown', 'downtown')
        assert result.zoneA == result.zoneB
        assert result.aqiA == result.aqiB
        assert result.difference == 0
    
    def test_get_history_success(self, service):
        start = datetime.now() - timedelta(days=3)
        end = datetime.now()
        
        result = service.get_history('downtown', start, end, 'daily')
        assert result is not None
        assert result.zone == 'downtown'
        assert result.granularity == 'daily'
        assert len(result.data_points) > 0
    
    def test_get_history_invalid_granularity(self, service):
        start = datetime.now() - timedelta(days=1)
        end = datetime.now()
        
        with pytest.raises(Fault) as exc:
            service.get_history('downtown', start, end, 'weekly')
        assert 'Granularité' in str(exc.value.faultstring)
    
    def test_get_history_invalid_dates(self, service):
        start = datetime.now()
        end = datetime.now() - timedelta(days=1)
        
        with pytest.raises(Fault) as exc:
            service.get_history('downtown', start, end, 'daily')
        assert 'date' in str(exc.value.faultstring).lower()
    
    def test_filter_pollutants_success(self, service):
        result = service.filter_pollutants('downtown', 30.0)
        assert result is not None
        assert result.zone == 'downtown'
        
        for pollutant in result.pollutants:
            assert pollutant.value > 30.0
    
    def test_filter_pollutants_high_threshold(self, service):
        result = service.filter_pollutants('park', 1000.0)
        assert result is not None
        assert len(result.pollutants) == 0
    
    def test_filter_pollutants_negative_threshold(self, service):
        with pytest.raises(Fault) as exc:
            service.filter_pollutants('downtown', -10.0)
        assert 'négatif' in str(exc.value.faultstring).lower()
    
    def test_health_check(self, service):
        result = service.health_check()
        assert result is not None
        assert result.status in ['UP', 'DOWN', 'DEGRADED']
        assert result.version == '1.0.0'
        assert result.uptime_seconds >= 0
        assert result.database_status in ['UP', 'DOWN']
    
    def test_aqi_categories(self, service):
        assert service._get_aqi_category(30) == 'Good'
        assert service._get_aqi_category(75) == 'Moderate'
        assert service._get_aqi_category(125) == 'Unhealthy for Sensitive Groups'
        assert service._get_aqi_category(175) == 'Unhealthy'
        assert service._get_aqi_category(250) == 'Very Unhealthy'
        assert service._get_aqi_category(350) == 'Hazardous'