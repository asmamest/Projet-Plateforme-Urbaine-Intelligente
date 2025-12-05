"""
Tests unitaires pour le service
"""
import pytest
from datetime import datetime
from repositories.data_repository import DataRepository
from services.event_service import EventService


@pytest.fixture
def service():
    """Fixture pour créer un service"""
    repo = DataRepository()
    return EventService(repo)


def test_get_all_zones(service):
    """Test récupération de toutes les zones via service"""
    zones = service.get_all_zones()
    assert len(zones) > 0


def test_get_zone(service):
    """Test récupération d'une zone via service"""
    zone = service.get_zone("zone-1")
    assert zone is not None
    assert zone.id == "zone-1"


def test_get_all_events(service):
    """Test récupération de tous les événements"""
    events = service.get_all_events()
    assert len(events) > 0


def test_create_event_success(service):
    """Test création d'événement réussie"""
    event = service.create_event(
        name="Test Service Event",
        description="Test via service",
        event_type_id="type-1",
        zone_id="zone-1",
        date=datetime.now().isoformat(),
        priority="MEDIUM",
        status="PENDING"
    )
    assert event is not None
    assert event.name == "Test Service Event"


def test_create_event_invalid_type(service):
    """Test création avec type invalide"""
    with pytest.raises(ValueError):
        service.create_event(
            name="Test",
            description="Test",
            event_type_id="invalid-type",
            zone_id="zone-1",
            date=datetime.now().isoformat(),
            priority="MEDIUM"
        )


def test_create_event_invalid_zone(service):
    """Test création avec zone invalide"""
    with pytest.raises(ValueError):
        service.create_event(
            name="Test",
            description="Test",
            event_type_id="type-1",
            zone_id="invalid-zone",
            date=datetime.now().isoformat(),
            priority="MEDIUM"
        )


def test_update_event(service):
    """Test mise à jour via service"""
    event = service.create_event(
        name="Original",
        description="Original",
        event_type_id="type-1",
        zone_id="zone-1",
        date=datetime.now().isoformat(),
        priority="LOW"
    )
    
    updated = service.update_event(
        event.id,
        name="Updated Name",
        priority="HIGH"
    )
    
    assert updated.name == "Updated Name"
    assert updated.priority.value == "HIGH"


def test_delete_event(service):
    """Test suppression via service"""
    event = service.create_event(
        name="To Delete",
        description="Will be deleted",
        event_type_id="type-1",
        zone_id="zone-1",
        date=datetime.now().isoformat(),
        priority="LOW"
    )
    
    result = service.delete_event(event.id)
    assert result is True


def test_filter_events(service):
    """Test filtrage des événements"""
    events = service.filter_events(priority="CRITICAL")
    assert all(e.priority.value == "CRITICAL" for e in events)
