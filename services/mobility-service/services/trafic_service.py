"""
Service métier pour l'état du trafic
"""
from typing import List
from repositories.trafic_repository import TraficRepository
from models.entities import EtatTrafic

class TraficService:
    """Service de gestion du trafic"""
    
    def __init__(self):
        self.repository = TraficRepository()
    
    def get_all_trafic(self) -> List[EtatTrafic]:
        """Récupère l'état du trafic de toutes les lignes"""
        return self.repository.find_all()