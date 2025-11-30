"""
Schémas Pydantic pour l'état du trafic
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TraficItem(BaseModel):
    """État du trafic pour une ligne"""
    ligne_id: str
    statut: str = Field(..., description="État du trafic", example="normal")
    retard_minutes: int = Field(0, description="Retard en minutes")
    message: str = Field("", description="Message d'information")
    timestamp: datetime

class TraficResponse(BaseModel):
    """Réponse globale de l'état du trafic"""
    derniere_maj: datetime
    nombre_lignes: int
    trafic: List[TraficItem]
