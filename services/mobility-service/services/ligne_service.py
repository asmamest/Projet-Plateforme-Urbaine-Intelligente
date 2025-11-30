"""
Service métier pour la gestion des lignes
"""
from typing import List, Optional
from repositories.ligne_repository import LigneRepository
from models.entities import Ligne, TypeTransport
from schemas.ligne import LigneCreate, LigneUpdate

class LigneService:
    """Service de gestion des lignes de transport"""
    
    def __init__(self):
        self.repository = LigneRepository()
    
    def get_all_lignes(self) -> List[Ligne]:
        """Récupère toutes les lignes"""
        return self.repository.find_all()
    
    def get_ligne_by_id(self, id: str) -> Optional[Ligne]:
        """Récupère une ligne par son ID"""
        return self.repository.find_by_id(id)
    
    def create_ligne(self, data: LigneCreate) -> Ligne:
        """Crée une nouvelle ligne"""
        ligne = Ligne(
            id="",  # Sera généré par le repository
            numero=data.numero,
            nom=data.nom,
            type_transport=TypeTransport(data.type_transport),
            terminus_debut=data.terminus_debut,
            terminus_fin=data.terminus_fin,
            actif=data.actif
        )
        return self.repository.create(ligne)
    
    def update_ligne(self, id: str, data: LigneUpdate) -> Optional[Ligne]:
        """Met à jour une ligne existante"""
        existing = self.repository.find_by_id(id)
        if not existing:
            return None
        
        # Mise à jour des champs fournis
        if data.numero is not None:
            existing.numero = data.numero
        if data.nom is not None:
            existing.nom = data.nom
        if data.type_transport is not None:
            existing.type_transport = TypeTransport(data.type_transport)
        if data.terminus_debut is not None:
            existing.terminus_debut = data.terminus_debut
        if data.terminus_fin is not None:
            existing.terminus_fin = data.terminus_fin
        if data.actif is not None:
            existing.actif = data.actif
        
        return self.repository.update(id, existing)
    
    def delete_ligne(self, id: str) -> bool:
        """Supprime une ligne"""
        return self.repository.delete(id)
