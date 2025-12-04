"""
Repository pour accès aux données
"""
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from utils.logger import setup_logger

logger = setup_logger('repository', 'logs/service.log')


class DataRepository:
    
    def __init__(self):
        self.data_source = os.getenv('DATA_SOURCE', 'data/air_quality_data.csv')
        self.data_cache = {}
        self._load_data()
    
    def _load_data(self):
        """Charger les données depuis CSV"""
        try:
            if not os.path.exists(self.data_source):
                logger.warning(f"Fichier {self.data_source} introuvable, données mock")
                self._load_mock_data()
                return
            
            with open(self.data_source, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    zone = row['zone']
                    self.data_cache[zone] = {
                        'aqi': int(row['aqi']),
                        'pm25': float(row['pm25']),
                        'pm10': float(row['pm10']),
                        'no2': float(row['no2']),
                        'co2': float(row['co2']),
                        'o3': float(row['o3']),
                        'so2': float(row['so2'])
                    }
            logger.info(f"Données chargées: {len(self.data_cache)} zones")
        except Exception as e:
            logger.error(f"Erreur chargement: {str(e)}")
            self._load_mock_data()
    
    def _load_mock_data(self):
        """Charger données mock"""
        self.data_cache = {
            'downtown': {
                'aqi': 85, 'pm25': 28.5, 'pm10': 45.2,
                'no2': 42.1, 'co2': 410.0, 'o3': 35.8, 'so2': 8.3
            },
            'industrial': {
                'aqi': 142, 'pm25': 65.3, 'pm10': 98.7,
                'no2': 78.9, 'co2': 520.0, 'o3': 55.2, 'so2': 28.4
            },
            'residential': {
                'aqi': 62, 'pm25': 18.2, 'pm10': 32.1,
                'no2': 25.6, 'co2': 380.0, 'o3': 28.4, 'so2': 5.2
            },
            'park': {
                'aqi': 35, 'pm25': 8.5, 'pm10': 15.3,
                'no2': 12.4, 'co2': 350.0, 'o3': 22.1, 'so2': 2.8
            }
        }
        logger.info("Données mock chargées")
    
    def get_current_data(self, zone: str) -> Optional[Dict]:
        """Obtenir données actuelles pour une zone"""
        return self.data_cache.get(zone)
    
    def get_historical_data(self, zone: str, start_date, end_date, granularity: str) -> List[Dict]:
        """Générer données historiques simulées"""
        if zone not in self.data_cache:
            return []
        
        base_data = self.data_cache[zone]
        history = []
        
        current = start_date
        delta = timedelta(hours=1) if granularity == 'hourly' else timedelta(days=1)
        
        while current <= end_date:
            import random
            entry = {
                'timestamp': current,
                'aqi': int(base_data['aqi'] * random.uniform(0.8, 1.2)),
                'pm25': base_data['pm25'] * random.uniform(0.7, 1.3),
                'pm10': base_data['pm10'] * random.uniform(0.7, 1.3),
                'no2': base_data['no2'] * random.uniform(0.7, 1.3),
                'co2': base_data['co2'] * random.uniform(0.9, 1.1),
                'o3': base_data['o3'] * random.uniform(0.7, 1.3),
                'so2': base_data['so2'] * random.uniform(0.7, 1.3)
            }
            history.append(entry)
            current += delta
            
            if len(history) >= 100:
                break
        
        return history
    
    def check_health(self) -> bool:
        """Vérifier état du repository"""
        return len(self.data_cache) > 0