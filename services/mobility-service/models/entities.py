"""
Entités du domaine métier (modèles internes)
"""
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatutTrafic(str, Enum):
    NORMAL = "normal"
    RETARD = "retard"
    ANNULE = "annule"
    PERTURBE = "perturbe"

class TypeTransport(str, Enum):
    BUS = "bus"
    METRO = "metro"
    TRAIN = "train"
    TRAMWAY = "tramway"

class Ligne:
    """Entité représentant une ligne de transport"""
    def __init__(
        self,
        id: str,
        numero: str,
        nom: str,
        type_transport: TypeTransport,
        terminus_debut: str,
        terminus_fin: str,
        actif: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.numero = numero
        self.nom = nom
        self.type_transport = type_transport
        self.terminus_debut = terminus_debut
        self.terminus_fin = terminus_fin
        self.actif = actif
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

class Horaire:
    """Entité représentant un horaire de passage"""
    def __init__(
        self,
        id: str,
        ligne_id: str,
        destination: str,
        heure_depart: str,
        heure_arrivee: str,
        station: str,
        quai: str
    ):
        self.id = id
        self.ligne_id = ligne_id
        self.destination = destination
        self.heure_depart = heure_depart
        self.heure_arrivee = heure_arrivee
        self.station = station
        self.quai = quai

class EtatTrafic:
    """Entité représentant l'état du trafic"""
    def __init__(
        self,
        ligne_id: str,
        statut: StatutTrafic,
        retard_minutes: int = 0,
        message: str = "",
        timestamp: Optional[datetime] = None
    ):
        self.ligne_id = ligne_id
        self.statut = statut
        self.retard_minutes = retard_minutes
        self.message = message
        self.timestamp = timestamp or datetime.now()

class Disponibilite:
    """Entité représentant la disponibilité des véhicules"""
    def __init__(
        self,
        ligne_id: str,
        vehicules_total: int,
        vehicules_en_service: int,
        taux_disponibilite: float,
        derniere_maj: Optional[datetime] = None
    ):
        self.ligne_id = ligne_id
        self.vehicules_total = vehicules_total
        self.vehicules_en_service = vehicules_en_service
        self.taux_disponibilite = taux_disponibilite
        self.derniere_maj = derniere_maj or datetime.now()