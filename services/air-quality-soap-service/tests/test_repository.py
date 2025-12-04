"""
Tests unitaires pour DataRepository
"""
import pytest
import os
from datetime import datetime, timedelta

from repositories.data_repository import DataRepository


class TestDataRepository:
    
    @pytest.fixture
    def repo(self):
        return DataRepository()
    
    def test_initialization(self, repo):
        assert repo is not None
        assert repo.data_cache is not None
        assert len(repo.data_cache) > 0
    
    def test_get_current_data_success(self, repo):
        data = repo.get_current_data('downtown')
        assert data is not None
        assert 'aqi' in data
        assert 'pm25' in data
        assert 'pm10' in data
        assert 'no2' in data
        assert 'co2' in data
        assert 'o3' in data
        assert 'so2' in data
    
    def test_get_current_data_all_zones(self, repo):
        zones = ['downtown', 'industrial', 'residential', 'park']
        for zone in zones:
            data = repo.get_current_data(zone)
            assert data is not None
            assert isinstance(data['aqi'], int)
            assert data['aqi'] >= 0
    
    def test_get_current_data_invalid_zone(self, repo):
        data = repo.get_current_data('nonexistent')
        assert data is None
    
    def test_get_historical_data_hourly(self, repo):
        start = datetime.now() - timedelta(hours=24)
        end = datetime.now()
        
        history = repo.get_historical_data('downtown', start, end, 'hourly')
        assert history is not None
        assert len(history) > 0
        
        for entry in history:
            assert 'timestamp' in entry
            assert 'aqi' in entry
            assert entry['aqi'] > 0
    
    def test_get_historical_data_daily(self, repo):
        start = datetime.now() - timedelta(days=7)
        end = datetime.now()
        
        history = repo.get_historical_data('downtown', start, end, 'daily')
        assert history is not None
        assert len(history) > 0
    
    def test_get_historical_data_invalid_zone(self, repo):
        start = datetime.now() - timedelta(days=1)
        end = datetime.now()
        
        history = repo.get_historical_data('invalid', start, end, 'daily')
        assert history == []
    
    def test_check_health(self, repo):
        status = repo.check_health()
        assert status is True
    
    def test_data_structure(self, repo):
        for zone, data in repo.data_cache.items():
            assert isinstance(zone, str)
            assert isinstance(data, dict)
            assert all(isinstance(v, (int, float)) for v in data.values())