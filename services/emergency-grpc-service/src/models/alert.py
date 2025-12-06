"""
Modèles de données pour les alertes d'urgence
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class AlertType(Enum):
    """Types d'alertes d'urgence"""
    ACCIDENT = "ACCIDENT"
    FIRE = "FIRE"
    AMBULANCE_REQUEST = "AMBULANCE_REQUEST"
    MEDICAL_EMERGENCY = "MEDICAL_EMERGENCY"
    NATURAL_DISASTER = "NATURAL_DISASTER"
    SECURITY_THREAT = "SECURITY_THREAT"
    PUBLIC_HEALTH = "PUBLIC_HEALTH"


class Priority(Enum):
    """Niveaux de priorité"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AlertStatus(Enum):
    """Statuts des alertes"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"


@dataclass
class Location:
    """Localisation géographique"""
    latitude: float
    longitude: float
    address: str
    city: str
    zone: str
    
    def __post_init__(self):
        """Validation des coordonnées GPS"""
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Invalid longitude: {self.longitude}")
        if not self.address or not self.address.strip():
            raise ValueError("Address cannot be empty")
        if not self.city or not self.city.strip():
            raise ValueError("City cannot be empty")
        if not self.zone or not self.zone.strip():
            raise ValueError("Zone cannot be empty")


@dataclass
class Alert:
    """Alerte d'urgence"""
    alert_type: AlertType
    description: str
    location: Location
    priority: Priority
    reporter_name: str
    reporter_phone: str
    affected_people: int
    alert_id: str = field(default_factory=lambda: f"ALERT-{uuid.uuid4().hex[:12].upper()}")
    status: AlertStatus = AlertStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    assigned_team: Optional[str] = None
    notes: Optional[str] = None
    
    def update_status(self, new_status: AlertStatus, assigned_team: Optional[str] = None, 
                      notes: Optional[str] = None):
        """Met à jour le statut de l'alerte"""
        self.status = new_status
        if assigned_team:
            self.assigned_team = assigned_team
        if notes:
            self.notes = notes
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            "alert_id": self.alert_id,
            "alert_type": self.alert_type.value,
            "description": self.description,
            "location": {
                "latitude": self.location.latitude,
                "longitude": self.location.longitude,
                "address": self.location.address,
                "city": self.location.city,
                "zone": self.location.zone
            },
            "priority": self.priority.value,
            "status": self.status.value,
            "reporter_name": self.reporter_name,
            "reporter_phone": self.reporter_phone,
            "affected_people": self.affected_people,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "assigned_team": self.assigned_team,
            "notes": self.notes
        }