"""
Repository pour l'état du trafic
"""
from typing import List, Dict
from models.entities import EtatTrafic, StatutTrafic
from datetime import datetime

class TraficRepository:
    """Repository en mémoire pour l'état du trafic"""
    
    def __init__(self):
        self._storage: Dict[str, EtatTrafic] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialise des états de trafic mockés"""
        self._storage = {
            "1": EtatTrafic("1", StatutTrafic.NORMAL, 0, "Trafic fluide", datetime.now()),
            "2": EtatTrafic("2", StatutTrafic.RETARD, 5, "Retard dû à un incident technique", datetime.now()),
            "3": EtatTrafic("3", StatutTrafic.NORMAL, 0, "Circulation normale", datetime.now()),
            "4": EtatTrafic("4", StatutTrafic.PERTURBE, 10, "Travaux sur la voie", datetime.now()),
        }
    
    def find_all(self) -> List[EtatTrafic]:
        """Récupère l'état du trafic de toutes les lignes"""
        return list(self._storage.values())
    
    def find_by_ligne(self, ligne_id: str) -> EtatTrafic:
        """Récupère l'état du trafic d'une ligne spécifique"""
        return self._storage.get(ligne_id, EtatTrafic(ligne_id, StatutTrafic.NORMAL, 0, ""))
