"""
Types GraphQL
"""
import graphene


class ZoneType(graphene.ObjectType):
    """Type GraphQL pour Zone"""
    id = graphene.String(description="ID unique de la zone")
    name = graphene.String(description="Nom de la zone")
    description = graphene.String(description="Description de la zone")


class EventTypeType(graphene.ObjectType):
    """Type GraphQL pour EventType"""
    id = graphene.String(description="ID unique du type d'événement")
    name = graphene.String(description="Nom du type")
    description = graphene.String(description="Description du type")


class EventType(graphene.ObjectType):
    """Type GraphQL pour Event"""
    id = graphene.String(description="ID unique de l'événement")
    name = graphene.String(description="Nom de l'événement")
    description = graphene.String(description="Description détaillée")
    event_type_id = graphene.String(description="ID du type d'événement")
    zone_id = graphene.String(description="ID de la zone")
    date = graphene.String(description="Date de l'événement (ISO format)")
    priority = graphene.String(description="Priorité: LOW, MEDIUM, HIGH, CRITICAL")
    status = graphene.String(description="Statut: PENDING, IN_PROGRESS, RESOLVED, CANCELLED")
    created_at = graphene.String(description="Date de création")
    updated_at = graphene.String(description="Date de dernière mise à jour")
    
    # Relations
    event_type = graphene.Field(EventTypeType, description="Type d'événement complet")
    zone = graphene.Field(ZoneType, description="Zone complète")
    
    def resolve_event_type(self, info):
        """Résout la relation vers EventType"""
        service = info.context["event_service"]
        return service.get_event_type(self.event_type_id)
    
    def resolve_zone(self, info):
        """Résout la relation vers Zone"""
        service = info.context["event_service"]
        return service.get_zone(self.zone_id)
    
    def resolve_date(self, info):
        """Formate la date en ISO"""
        return self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date)
    
    def resolve_created_at(self, info):
        """Formate created_at en ISO"""
        return self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at)
    
    def resolve_updated_at(self, info):
        """Formate updated_at en ISO"""
        if self.updated_at:
            return self.updated_at.isoformat() if hasattr(self.updated_at, 'isoformat') else str(self.updated_at)
        return None
