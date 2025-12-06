"""
Tests unitaires pour AlertValidator
"""
import pytest

from src.validators.alert_validator import AlertValidator


def test_validate_description_valid():
    """Test validation description valide"""
    AlertValidator.validate_description("This is a valid description with enough characters")
    # Pas d'exception = succès


def test_validate_description_too_short():
    """Test description trop courte"""
    with pytest.raises(ValueError):
        AlertValidator.validate_description("Short")


def test_validate_description_too_long():
    """Test description trop longue"""
    with pytest.raises(ValueError):
        AlertValidator.validate_description("x" * 1001)


def test_validate_phone_valid():
    """Test téléphone valide"""
    AlertValidator.validate_phone("+33612345678")
    AlertValidator.validate_phone("+1234567890")
    # Pas d'exception = succès


def test_validate_phone_invalid():
    """Test téléphone invalide"""
    with pytest.raises(ValueError):
        AlertValidator.validate_phone("invalid")
    
    with pytest.raises(ValueError):
        AlertValidator.validate_phone("123")


def test_validate_location_valid():
    """Test localisation valide"""
    AlertValidator.validate_location(
        48.8566, 2.3522,
        "123 Test Street",
        "Paris",
        "Zone Centre"
    )
    # Pas d'exception = succès


def test_validate_location_invalid_latitude():
    """Test latitude invalide"""
    with pytest.raises(ValueError):
        AlertValidator.validate_location(
            91.0, 2.3522,
            "123 Test Street",
            "Paris",
            "Zone Centre"
        )


def test_validate_location_invalid_longitude():
    """Test longitude invalide"""
    with pytest.raises(ValueError):
        AlertValidator.validate_location(
            48.8566, 181.0,
            "123 Test Street",
            "Paris",
            "Zone Centre"
        )


def test_validate_reporter_name_valid():
    """Test nom rapporteur valide"""
    AlertValidator.validate_reporter_name("John Doe")
    # Pas d'exception = succès


def test_validate_reporter_name_too_short():
    """Test nom rapporteur trop court"""
    with pytest.raises(ValueError):
        AlertValidator.validate_reporter_name("A")


def test_validate_affected_people_valid():
    """Test nombre personnes affectées valide"""
    AlertValidator.validate_affected_people(0)
    AlertValidator.validate_affected_people(10)
    # Pas d'exception = succès


def test_validate_affected_people_negative():
    """Test nombre personnes affectées négatif"""
    with pytest.raises(ValueError):
        AlertValidator.validate_affected_people(-1)
