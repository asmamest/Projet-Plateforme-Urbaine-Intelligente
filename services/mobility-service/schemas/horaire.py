"""
Schémas Pydantic pour les horaires
"""
from pydantic import BaseModel, Field
from typing import List

class HoraireItem(BaseModel):
    """Schéma représentant un horaire de passage"""
    id: str
    ligne_id: str
    destination: str = Field(..., example="Centre-Ville")
    heure_depart: str = Field(..., example="08:15")
    heure_arrivee: str = Field(..., example="08:40")
    station: str = Field(..., example="Gare Sud")
    quai: str = Field(..., example="A")

class HorairesResponse(BaseModel):
    """Réponse contenant la liste des horaires"""
    ligne: str = Field(..., description="Numéro de la ligne")
    nombre_horaires: int
    horaires: List[HoraireItem]
