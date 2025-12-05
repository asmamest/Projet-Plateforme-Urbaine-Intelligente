"""
Schéma GraphQL - Queries
"""
import graphene
from typing import Optional
from graphql_schemas.types import EventType, ZoneType, EventTypeType


class Query(graphene.ObjectType):
    """Root Query pour les événements urbains"""
    
    # Zones
    zones = graphene.List(
        ZoneType,
        description="Liste de toutes les zones urbaines"
    )
    zone = graphene.Field(
        ZoneType,
        zone_id=graphene.String(required=True),
        description="Récupère une zone par son ID"
    )
    
    # Types d'événements
    event_types = graphene.List(
        EventTypeType,
        description="Liste de tous les types d'événements"
    )
    event_type = graphene.Field(
        EventTypeType,
        type_id=graphene.String(required=True),
        description="Récupère un type d'événement par son ID"
    )
    
    # Événements
    events = graphene.List(
        EventType,
        event_type_id=graphene.String(),
        zone_id=graphene.String(),
        status=graphene.String(),
        priority=graphene.String(),
        date_from=graphene.String(),
        date_to=graphene.String(),
        description="Liste des événements avec filtres optionnels"
    )
    event = graphene.Field(
        EventType,
        event_id=graphene.String(required=True),
        description="Récupère un événement par son ID"
    )
    
    def resolve_zones(self, info):
        """Résolveur pour la liste des zones"""
        service = info.context["event_service"]
        return service.get_all_zones()
    
    def resolve_zone(self, info, zone_id):
        """Résolveur pour une zone spécifique"""
        service = info.context["event_service"]
        return service.get_zone(zone_id)
    
    def resolve_event_types(self, info):
        """Résolveur pour la liste des types d'événements"""
        service = info.context["event_service"]
        return service.get_all_event_types()
    
    def resolve_event_type(self, info, type_id):
        """Résolveur pour un type d'événement spécifique"""
        service = info.context["event_service"]
        return service.get_event_type(type_id)
    
    def resolve_events(
        self,
        info,
        event_type_id=None,
        zone_id=None,
        status=None,
        priority=None,
        date_from=None,
        date_to=None
    ):
        """Résolveur pour la liste des événements avec filtres"""
        service = info.context["event_service"]
        
        if any([event_type_id, zone_id, status, priority, date_from, date_to]):
            return service.filter_events(
                event_type_id=event_type_id,
                zone_id=zone_id,
                status=status,
                priority=priority,
                date_from=date_from,
                date_to=date_to
            )
        return service.get_all_events()
    
    def resolve_event(self, info, event_id):
        """Résolveur pour un événement spécifique"""
        service = info.context["event_service"]
        return service.get_event(event_id)

