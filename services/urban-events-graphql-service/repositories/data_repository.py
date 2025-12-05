"""
Repository pour la gestion des données (Mock avec possibilité d'extension DB)
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models.event_models import Event, Zone, EventType, EventStatus, Priority
import uuid


class DataRepository:
    """
    Repository pour gérer les données des événements.
    Actuellement avec mock data, facilement extensible vers une vraie DB.
    """
    
    def __init__(self):
        """Initialisation avec données mockées"""
        self._zones: Dict[str, Zone] = {}
        self._event_types: Dict[str, EventType] = {}
        self._events: Dict[str, Event] = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialisation des données mockées"""
        # Zones
        zones_data = [
            Zone("zone-1", "Centre-Ville", "Zone du centre historique"),
            Zone("zone-2", "Quartier Nord", "Zone résidentielle nord"),
            Zone("zone-3", "Zone Industrielle", "Zone d'activité industrielle"),
            Zone("zone-4", "Bord de Mer", "Zone côtière et touristique"),
        ]
        for zone in zones_data:
            self._zones[zone.id] = zone
        
        # Types d'événements
        event_types_data = [
            EventType("type-1", "Accident", "Accident de circulation"),
            EventType("type-2", "Travaux", "Travaux publics"),
            EventType("type-3", "Manifestation", "Événement public ou manifestation"),
            EventType("type-4", "Urgence", "Situation d'urgence"),
            EventType("type-5", "Pollution", "Alerte pollution"),
        ]
        for event_type in event_types_data:
            self._event_types[event_type.id] = event_type
        
        # Événements
        now = datetime.now()
        events_data = [
            Event(
                "event-1",
                "Accident Boulevard Principal",
                "Collision entre deux véhicules",
                "type-1",
                "zone-1",
                now - timedelta(hours=2),
                Priority.HIGH,
                EventStatus.IN_PROGRESS,
                now - timedelta(hours=2)
            ),
            Event(
                "event-2",
                "Travaux Rue de la Paix",
                "Réfection de la chaussée",
                "type-2",
                "zone-2",
                now + timedelta(days=1),
                Priority.MEDIUM,
                EventStatus.PENDING,
                now - timedelta(days=5)
            ),
            Event(
                "event-3",
                "Festival d'été",
                "Grand festival culturel annuel",
                "type-3",
                "zone-4",
                now + timedelta(days=15),
                Priority.LOW,
                EventStatus.PENDING,
                now - timedelta(days=30)
            ),
            Event(
                "event-4",
                "Alerte Pollution Ozone",
                "Pic de pollution à l'ozone",
                "type-5",
                "zone-3",
                now,
                Priority.CRITICAL,
                EventStatus.IN_PROGRESS,
                now - timedelta(hours=1)
            ),
        ]
        for event in events_data:
            self._events[event.id] = event
    
    # ========== ZONES ==========
    
    def get_all_zones(self) -> List[Zone]:
        """Récupère toutes les zones"""
        return list(self._zones.values())
    
    def get_zone_by_id(self, zone_id: str) -> Optional[Zone]:
        """Récupère une zone par son ID"""
        return self._zones.get(zone_id)
    
    # ========== EVENT TYPES ==========
    
    def get_all_event_types(self) -> List[EventType]:
        """Récupère tous les types d'événements"""
        return list(self._event_types.values())
    
    def get_event_type_by_id(self, type_id: str) -> Optional[EventType]:
        """Récupère un type d'événement par son ID"""
        return self._event_types.get(type_id)
    
    # ========== EVENTS ==========
    
    def get_all_events(self) -> List[Event]:
        """Récupère tous les événements"""
        return list(self._events.values())
    
    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """Récupère un événement par son ID"""
        return self._events.get(event_id)
    
    def filter_events(
        self,
        event_type_id: Optional[str] = None,
        zone_id: Optional[str] = None,
        status: Optional[EventStatus] = None,
        priority: Optional[Priority] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[Event]:
        """Filtre les événements selon plusieurs critères"""
        events = self.get_all_events()
        
        if event_type_id:
            events = [e for e in events if e.event_type_id == event_type_id]
        if zone_id:
            events = [e for e in events if e.zone_id == zone_id]
        if status:
            events = [e for e in events if e.status == status]
        if priority:
            events = [e for e in events if e.priority == priority]
        if date_from:
            events = [e for e in events if e.date >= date_from]
        if date_to:
            events = [e for e in events if e.date <= date_to]
        
        return events
    
    def create_event(
        self,
        name: str,
        description: str,
        event_type_id: str,
        zone_id: str,
        date: datetime,
        priority: Priority,
        status: EventStatus = EventStatus.PENDING
    ) -> Event:
        """Crée un nouvel événement"""
        event_id = f"event-{uuid.uuid4().hex[:8]}"
        event = Event(
            id=event_id,
            name=name,
            description=description,
            event_type_id=event_type_id,
            zone_id=zone_id,
            date=date,
            priority=priority,
            status=status,
            created_at=datetime.now()
        )
        self._events[event_id] = event
        return event
    
    def update_event(
        self,
        event_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        event_type_id: Optional[str] = None,
        zone_id: Optional[str] = None,
        date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        status: Optional[EventStatus] = None
    ) -> Optional[Event]:
        """Met à jour un événement existant"""
        event = self._events.get(event_id)
        if not event:
            return None
        
        if name is not None:
            event.name = name
        if description is not None:
            event.description = description
        if event_type_id is not None:
            event.event_type_id = event_type_id
        if zone_id is not None:
            event.zone_id = zone_id
        if date is not None:
            event.date = date
        if priority is not None:
            event.priority = priority
        if status is not None:
            event.status = status
        
        event.updated_at = datetime.now()
        return event
    
    def delete_event(self, event_id: str) -> bool:
        """Supprime un événement"""
        if event_id in self._events:
            del self._events[event_id]
            return True
        return False
