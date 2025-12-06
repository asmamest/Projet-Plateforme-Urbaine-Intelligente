"""
Validateurs pour les alertes d'urgence
"""
import re
import grpc


class AlertValidator:
    """Validation stricte des données d'alerte"""
    
    PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{1,14}$')
    
    @staticmethod
    def validate_description(description: str):
        """Valide la description (10-1000 caractères)"""
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        
        if len(description) < 10:
            raise ValueError("Description must be at least 10 characters")
        
        if len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
    
    @staticmethod
    def validate_phone(phone: str):
        """Valide le numéro de téléphone (format E.164)"""
        if not phone or not phone.strip():
            raise ValueError("Phone number cannot be empty")
        
        cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if not AlertValidator.PHONE_PATTERN.match(cleaned):
            raise ValueError(f"Invalid phone number format: {phone}")
    
    @staticmethod
    def validate_location(latitude: float, longitude: float, address: str, city: str, zone: str):
        """Valide la localisation"""
        if not -90 <= latitude <= 90:
            raise ValueError(f"Invalid latitude: {latitude}")
        
        if not -180 <= longitude <= 180:
            raise ValueError(f"Invalid longitude: {longitude}")
        
        if not address or not address.strip():
            raise ValueError("Address cannot be empty")
        
        if not city or not city.strip():
            raise ValueError("City cannot be empty")
        
        if not zone or not zone.strip():
            raise ValueError("Zone cannot be empty")
    
    @staticmethod
    def validate_reporter_name(name: str):
        """Valide le nom du rapporteur"""
        if not name or not name.strip():
            raise ValueError("Reporter name cannot be empty")
        
        if len(name) < 2:
            raise ValueError("Reporter name must be at least 2 characters")
    
    @staticmethod
    def validate_affected_people(count: int):
        """Valide le nombre de personnes affectées"""
        if count < 0:
            raise ValueError("Affected people count cannot be negative")