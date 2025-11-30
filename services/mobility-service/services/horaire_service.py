"""
Service métier pour les horaires
"""
from typing import List
from repositories.horaire_repository import HoraireRepository
from repositories.ligne_repository import LigneRepository
from models.entities import Horaire

class HoraireService:
    """Service de gestion des horaires"""
    
    def __init__(self):
        self.repository = HoraireRepository()
        self.ligne_repository = LigneRepository()
    
    def get_horaires_by_ligne(self, ligne: str) -> List[Horaire]:
        """Récupère les horaires d'une ligne donnée"""
        # Vérification que la ligne existe
        ligne_entity = self.ligne_repository.find_by_numero(ligne)
        if not ligne_entity:
            return []
        
        return self.repository.find_by_ligne(ligne)
