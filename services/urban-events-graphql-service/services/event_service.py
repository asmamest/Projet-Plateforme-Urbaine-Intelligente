"""
Service métier pour la gestion des événements urbains
"""
from typing import List, Optional
from datetime import datetime
from repositories.data_repository import DataRepository
from models.event_models import Event, Zone, EventType, EventStatus, Priority


class EventService:
    """
    Service métier pour gérer la logique des événements urbains
    """
    
    def __init__(self, repository: DataRepository):
        self.repository = repository
    
    # ========== ZONES ==========
    
    def get_all_zones(self) -> List[Zone]:
        """Récupère toutes les zones"""
        return self.repository.get_all_zones()
    
    def get_zone(self, zone_id: str) -> Optional[Zone]:
        """Récupère une zone spécifique"""
        return self.repository.get_zone_by_id(zone_id)
    
    # ========== EVENT TYPES ==========
    
    def get_all_event_types(self) -> List[EventType]:
        """Récupère tous les types d'événements"""
        return self.repository.get_all_event_types()
    
    def get_event_type(self, type_id: str) -> Optional[EventType]:
        """Récupère un type d'événement spécifique"""
        return self.repository.get_event_type_by_id(type_id)
    
    # ========== EVENTS ==========
    
    def get_all_events(self) -> List[Event]:
        """Récupère tous les événements"""
        return self.repository.get_all_events()
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Récupère un événement spécifique"""
        return self.repository.get_event_by_id(event_id)
    
    def filter_events(
        self,
        event_type_id: Optional[str] = None,
        zone_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Event]:
        """Filtre les événements selon des critères"""
        # Conversion des strings en enums
        status_enum = EventStatus(status) if status else None
        priority_enum = Priority(priority) if priority else None
        date_from_dt = datetime.fromisoformat(date_from) if date_from else None
        date_to_dt = datetime.fromisoformat(date_to) if date_to else None
        
        return self.repository.filter_events(
            event_type_id=event_type_id,
            zone_id=zone_id,
            status=status_enum,
            priority=priority_enum,
            date_from=date_from_dt,
            date_to=date_to_dt
        )
    
    def create_event(
        self,
        name: str,
        description: str,
        event_type_id: str,
        zone_id: str,
        date: str,
        priority: str,
        status: str = "PENDING"
    ) -> Event:
        """Crée un nouvel événement"""
        # Validation
        if not self.repository.get_event_type_by_id(event_type_id):
            raise ValueError(f"Type d'événement invalide: {event_type_id}")
        if not self.repository.get_zone_by_id(zone_id):
            raise ValueError(f"Zone invalide: {zone_id}")
        
        date_dt = datetime.fromisoformat(date)
        priority_enum = Priority(priority)
        status_enum = EventStatus(status)
        
        return self.repository.create_event(
            name=name,
            description=description,
            event_type_id=event_type_id,
            zone_id=zone_id,
            date=date_dt,
            priority=priority_enum,
            status=status_enum
        )
    
    def update_event(
        self,
        event_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        event_type_id: Optional[str] = None,
        zone_id: Optional[str] = None,
        date: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[Event]:
        """Met à jour un événement"""
        # Validation si fournie
        if event_type_id and not self.repository.get_event_type_by_id(event_type_id):
            raise ValueError(f"Type d'événement invalide: {event_type_id}")
        if zone_id and not self.repository.get_zone_by_id(zone_id):
            raise ValueError(f"Zone invalide: {zone_id}")
        
        date_dt = datetime.fromisoformat(date) if date else None
        priority_enum = Priority(priority) if priority else None
        status_enum = EventStatus(status) if status else None
        
        return self.repository.update_event(
            event_id=event_id,
            name=name,
            description=description,
            event_type_id=event_type_id,
            zone_id=zone_id,
            date=date_dt,
            priority=priority_enum,
            status=status_enum
        )
    
    def delete_event(self, event_id: str) -> bool:
        """Supprime un événement"""
        return self.repository.delete_event(event_id)