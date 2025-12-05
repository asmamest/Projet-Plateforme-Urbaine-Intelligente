"""
Modèles de données pour les événements urbains
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class EventStatus(str, Enum):
    """Statut des événements"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CANCELLED = "CANCELLED"


class Priority(str, Enum):
    """Niveau de priorité"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Zone:
    """Zone géographique urbaine"""
    id: str
    name: str
    description: str
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


@dataclass
class EventType:
    """Type d'événement urbain"""
    id: str
    name: str
    description: str
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


@dataclass
class Event:
    """Événement urbain"""
    id: str
    name: str
    description: str
    event_type_id: str
    zone_id: str
    date: datetime
    priority: Priority
    status: EventStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "event_type_id": self.event_type_id,
            "zone_id": self.zone_id,
            "date": self.date.isoformat(),
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
