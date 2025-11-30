"""
Schémas Pydantic pour la disponibilité des véhicules
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class DisponibiliteItem(BaseModel):
    """Disponibilité pour une ligne"""
    ligne_id: str
    vehicules_total: int = Field(..., description="Nombre total de véhicules")
    vehicules_en_service: int = Field(..., description="Véhicules actuellement en service")
    taux_disponibilite: float = Field(..., description="Taux de disponibilité en %", ge=0, le=100)
    derniere_maj: datetime

class DisponibiliteResponse(BaseModel):
    """Réponse globale de disponibilité"""
    timestamp: datetime
    nombre_lignes: int
    disponibilites: List[DisponibiliteItem]
