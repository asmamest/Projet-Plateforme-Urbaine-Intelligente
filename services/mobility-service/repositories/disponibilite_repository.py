"""
Repository pour la disponibilité des véhicules
"""
from typing import List, Dict
from models.entities import Disponibilite
from datetime import datetime

class DisponibiliteRepository:
    """Repository en mémoire pour la disponibilité"""
    
    def __init__(self):
        self._storage: Dict[str, Disponibilite] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialise des disponibilités mockées"""
        self._storage = {
            "1": Disponibilite("1", 20, 18, 90.0, datetime.now()),
            "2": Disponibilite("2", 15, 12, 80.0, datetime.now()),
            "3": Disponibilite("3", 10, 9, 90.0, datetime.now()),
            "4": Disponibilite("4", 8, 7, 87.5, datetime.now()),
        }
    
    def find_all(self) -> List[Disponibilite]:
        """Récupère la disponibilité de toutes les lignes"""
        return list(self._storage.values())
    
    def find_by_ligne(self, ligne_id: str) -> Disponibilite:
        """Récupère la disponibilité d'une ligne spécifique"""
        return self._storage.get(ligne_id, Disponibilite(ligne_id, 0, 0, 0.0))