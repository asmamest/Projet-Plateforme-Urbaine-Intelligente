"""
Tests unitaires pour AlertRepository
"""
import pytest
from datetime import datetime, timedelta

from src.models.alert import Alert, Location, AlertType, Priority, AlertStatus
from src.repository.alert_repository import AlertRepository


def test_create_alert():
    """Test création d'alerte"""
    repo = AlertRepository()
    
    alert = Alert(
        alert_type=AlertType.FIRE,
        description="Test fire emergency",
        location=Location(48.8566, 2.3522, "123 Test St", "Paris", "Zone Test"),
        priority=Priority.HIGH,
        reporter_name="Test User",
        reporter_phone="+33612345678",
        affected_people=5
    )
    
    created = repo.create(alert)
    assert created.alert_id is not None
    assert created.status == AlertStatus.PENDING


def test_get_by_id():
    """Test récupération par ID"""
    repo = AlertRepository()
    
    alert = Alert(
        alert_type=AlertType.ACCIDENT,
        description="Test accident",
        location=Location(48.8566, 2.3522, "123 Test St", "Paris", "Zone Test"),
        priority=Priority.MEDIUM,
        reporter_name="Test User",
        reporter_phone="+33612345678",
        affected_people=2
    )
    
    created = repo.create(alert)
    retrieved = repo.get_by_id(created.alert_id)
    
    assert retrieved is not None
    assert retrieved.alert_id == created.alert_id


def test_update_alert():
    """Test mise à jour d'alerte"""
    repo = AlertRepository()
    
    alert = Alert(
        alert_type=AlertType.MEDICAL_EMERGENCY,
        description="Test medical emergency",
        location=Location(48.8566, 2.3522, "123 Test St", "Paris", "Zone Test"),
        priority=Priority.CRITICAL,
        reporter_name="Test User",
        reporter_phone="+33612345678",
        affected_people=1
    )
    
    created = repo.create(alert)
    created.update_status(AlertStatus.IN_PROGRESS, "Team Alpha", "On the way")
    
    updated = repo.update(created)
    
    assert updated.status == AlertStatus.IN_PROGRESS
    assert updated.assigned_team == "Team Alpha"
    assert updated.notes == "On the way"


def test_get_active_by_zone():
    """Test récupération alertes actives par zone"""
    repo = AlertRepository()
    
    # Les mock data existent déjà
    active = repo.get_active_by_zone("Zone Centre")
    
    assert len(active) > 0
    assert all(a.status in [AlertStatus.PENDING, AlertStatus.IN_PROGRESS] for a in active)


def test_get_active_by_zone_with_filters():
    """Test récupération avec filtres"""
    repo = AlertRepository()
    
    active = repo.get_active_by_zone(
        "Zone Nord",
        alert_type=AlertType.ACCIDENT,
        min_priority=Priority.HIGH
    )
    
    assert all(a.alert_type == AlertType.ACCIDENT for a in active)
    assert all(a.priority.value >= Priority.HIGH.value for a in active)


def test_get_history():
    """Test récupération historique"""
    repo = AlertRepository()
    
    history = repo.get_history(limit=10)
    
    assert len(history) <= 10
    # Vérifie tri chronologique décroissant
    if len(history) > 1:
        assert history[0].created_at >= history[1].created_at


def test_get_statistics():
    """Test génération statistiques"""
    repo = AlertRepository()
    
    stats = repo.get_statistics()
    
    assert "total" in stats
    assert stats["total"] > 0
    assert "pending" in stats
    assert "in_progress" in stats


def test_delete_alert():
    """Test suppression d'alerte"""
    repo = AlertRepository()
    
    alert = Alert(
        alert_type=AlertType.PUBLIC_HEALTH,
        description="Test public health alert",
        location=Location(48.8566, 2.3522, "123 Test St", "Paris", "Zone Test"),
        priority=Priority.LOW,
        reporter_name="Test User",
        reporter_phone="+33612345678",
        affected_people=0
    )
    
    created = repo.create(alert)
    deleted = repo.delete(created.alert_id)
    
    assert deleted is True
    assert repo.get_by_id(created.alert_id) is None