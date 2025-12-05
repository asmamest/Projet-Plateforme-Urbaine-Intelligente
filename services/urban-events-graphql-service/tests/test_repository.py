"""
Tests unitaires pour le repository
"""
import pytest
from datetime import datetime
from repositories.data_repository import DataRepository
from models.event_models import Priority, EventStatus


def test_get_all_zones():
    """Test récupération de toutes les zones"""
    repo = DataRepository()
    zones = repo.get_all_zones()
    assert len(zones) > 0
    assert zones[0].id is not None


def test_get_zone_by_id():
    """Test récupération d'une zone par ID"""
    repo = DataRepository()
    zone = repo.get_zone_by_id("zone-1")
    assert zone is not None
    assert zone.name == "Centre-Ville"


def test_get_all_event_types():
    """Test récupération de tous les types d'événements"""
    repo = DataRepository()
    types = repo.get_all_event_types()
    assert len(types) > 0


def test_create_event():
    """Test création d'un événement"""
    repo = DataRepository()
    event = repo.create_event(
        name="Test Event",
        description="Test Description",
        event_type_id="type-1",
        zone_id="zone-1",
        date=datetime.now(),
        priority=Priority.MEDIUM,
        status=EventStatus.PENDING
    )
    assert event.id is not None
    assert event.name == "Test Event"


def test_update_event():
    """Test mise à jour d'un événement"""
    repo = DataRepository()
    event = repo.create_event(
        name="Original",
        description="Original Description",
        event_type_id="type-1",
        zone_id="zone-1",
        date=datetime.now(),
        priority=Priority.LOW,
        status=EventStatus.PENDING
    )
    
    updated = repo.update_event(
        event.id,
        name="Updated",
        priority=Priority.HIGH
    )
    
    assert updated is not None
    assert updated.name == "Updated"
    assert updated.priority == Priority.HIGH
    assert updated.updated_at is not None


def test_delete_event():
    """Test suppression d'un événement"""
    repo = DataRepository()
    event = repo.create_event(
        name="To Delete",
        description="Will be deleted",
        event_type_id="type-1",
        zone_id="zone-1",
        date=datetime.now(),
        priority=Priority.LOW,
        status=EventStatus.PENDING
    )
    
    deleted = repo.delete_event(event.id)
    assert deleted is True
    
    retrieved = repo.get_event_by_id(event.id)
    assert retrieved is None


def test_filter_events_by_zone():
    """Test filtrage des événements par zone"""
    repo = DataRepository()
    events = repo.filter_events(zone_id="zone-1")
    assert all(e.zone_id == "zone-1" for e in events)


def test_filter_events_by_priority():
    """Test filtrage des événements par priorité"""
    repo = DataRepository()
    events = repo.filter_events(priority=Priority.CRITICAL)
    assert all(e.priority == Priority.CRITICAL for e in events)