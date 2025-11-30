"""
Schémas Pydantic pour les lignes de transport
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LigneBase(BaseModel):
    numero: str = Field(..., description="Numéro de la ligne", example="L1")
    nom: str = Field(..., description="Nom de la ligne", example="Centre-Ville - Banlieue")
    type_transport: str = Field(..., description="Type de transport", example="metro")
    terminus_debut: str = Field(..., description="Terminus de départ", example="Gare Centrale")
    terminus_fin: str = Field(..., description="Terminus d'arrivée", example="Aéroport")
    actif: bool = Field(True, description="Ligne active ou non")

class LigneCreate(LigneBase):
    """Schéma pour la création d'une ligne"""
    pass

class LigneUpdate(BaseModel):
    """Schéma pour la mise à jour d'une ligne"""
    numero: Optional[str] = None
    nom: Optional[str] = None
    type_transport: Optional[str] = None
    terminus_debut: Optional[str] = None
    terminus_fin: Optional[str] = None
    actif: Optional[bool] = None

class LigneResponse(LigneBase):
    """Schéma de réponse pour une ligne"""
    id: str = Field(..., description="Identifiant unique de la ligne")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True