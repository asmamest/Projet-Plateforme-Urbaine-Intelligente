"""
Repository pour la gestion des lignes de transport
"""
from typing import List, Optional, Dict
from repositories.base_repository import BaseRepository
from models.entities import Ligne, TypeTransport
from datetime import datetime
import uuid

class LigneRepository(BaseRepository[Ligne]):
    """Repository en mémoire pour les lignes (mock data)"""
    
    def __init__(self):
        # Base de données mockée en mémoire
        self._storage: Dict[str, Ligne] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialise des données de test"""
        lignes_mock = [
            Ligne("1", "L1", "Ligne 1 - Centre Nord", TypeTransport.METRO, "Gare Centrale", "Banlieue Nord", True),
            Ligne("2", "L2", "Ligne 2 - Est Ouest", TypeTransport.METRO, "Gare Est", "Gare Ouest", True),
            Ligne("3", "B15", "Bus 15 - Université", TypeTransport.BUS, "Centre-Ville", "Campus Universitaire", True),
            Ligne("4", "T1", "Tramway 1 - Côtier", TypeTransport.TRAMWAY, "Port", "Plage Sud", True),
        ]
        for ligne in lignes_mock:
            self._storage[ligne.id] = ligne
    
    def find_all(self) -> List[Ligne]:
        """Retourne toutes les lignes"""
        return list(self._storage.values())
    
    def find_by_id(self, id: str) -> Optional[Ligne]:
        """Trouve une ligne par son ID"""
        return self._storage.get(id)
    
    def find_by_numero(self, numero: str) -> Optional[Ligne]:
        """Trouve une ligne par son numéro"""
        for ligne in self._storage.values():
            if ligne.numero == numero:
                return ligne
        return None
    
    def create(self, ligne: Ligne) -> Ligne:
        """Crée une nouvelle ligne"""
        ligne.id = str(uuid.uuid4())
        ligne.created_at = datetime.now()
        ligne.updated_at = datetime.now()
        self._storage[ligne.id] = ligne
        return ligne
    
    def update(self, id: str, ligne: Ligne) -> Optional[Ligne]:
        """Met à jour une ligne existante"""
        if id not in self._storage:
            return None
        ligne.id = id
        ligne.updated_at = datetime.now()
        self._storage[id] = ligne
        return ligne
    
    def delete(self, id: str) -> bool:
        """Supprime une ligne"""
        if id in self._storage:
            del self._storage[id]
            return True
        return False
