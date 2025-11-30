"""
Service métier pour la disponibilité des véhicules
"""
from typing import List
from repositories.disponibilite_repository import DisponibiliteRepository
from models.entities import Disponibilite

class DisponibiliteService:
    """Service de gestion de la disponibilité"""
    
    def __init__(self):
        self.repository = DisponibiliteRepository()
    
    def get_all_disponibilites(self) -> List[Disponibilite]:
        """Récupère la disponibilité de toutes les lignes"""
        return self.repository.find_all()
    