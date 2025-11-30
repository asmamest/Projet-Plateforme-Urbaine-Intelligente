"""
Repository pour la gestion des horaires
"""
from typing import List, Dict
from models.entities import Horaire

class HoraireRepository:
    """Repository en mémoire pour les horaires"""
    
    def __init__(self):
        self._storage: Dict[str, List[Horaire]] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialise des horaires mockés"""
        self._storage = {
            "L1": [
                Horaire("h1", "1", "Banlieue Nord", "08:00", "08:25", "Gare Centrale", "A"),
                Horaire("h2", "1", "Banlieue Nord", "08:15", "08:40", "Gare Centrale", "A"),
                Horaire("h3", "1", "Gare Centrale", "08:30", "08:55", "Banlieue Nord", "B"),
            ],
            "L2": [
                Horaire("h4", "2", "Gare Ouest", "07:50", "08:15", "Gare Est", "1"),
                Horaire("h5", "2", "Gare Ouest", "08:20", "08:45", "Gare Est", "1"),
            ],
            "B15": [
                Horaire("h6", "3", "Campus Universitaire", "08:05", "08:30", "Centre-Ville", "C"),
                Horaire("h7", "3", "Centre-Ville", "08:35", "09:00", "Campus Universitaire", "D"),
            ],
        }
    
    def find_by_ligne(self, ligne: str) -> List[Horaire]:
        """Récupère tous les horaires d'une ligne"""
        return self._storage.get(ligne, [])
  
  