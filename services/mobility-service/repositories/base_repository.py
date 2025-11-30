"""
Repository de base avec pattern Repository abstrait
Facilite l'intégration future d'une vraie base de données
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Interface de base pour tous les repositories"""
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Récupère tous les éléments"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """Récupère un élément par son ID"""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Crée un nouvel élément"""
        pass
    
    @abstractmethod
    def update(self, id: str, entity: T) -> Optional[T]:
        """Met à jour un élément existant"""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Supprime un élément"""
        pass
