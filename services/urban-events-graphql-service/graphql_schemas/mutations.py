"""
Schéma GraphQL - Mutations
"""
import graphene
from graphql_schemas.types import EventType


class CreateEvent(graphene.Mutation):
    """Mutation pour créer un événement"""
    
    class Arguments:
        name = graphene.String(required=True, description="Nom de l'événement")
        description = graphene.String(required=True, description="Description")
        event_type_id = graphene.String(required=True, description="ID du type")
        zone_id = graphene.String(required=True, description="ID de la zone")
        date = graphene.String(required=True, description="Date ISO format")
        priority = graphene.String(required=True, description="LOW, MEDIUM, HIGH, CRITICAL")
        status = graphene.String(description="PENDING, IN_PROGRESS, RESOLVED, CANCELLED")
    
    event = graphene.Field(EventType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(
        self,
        info,
        name,
        description,
        event_type_id,
        zone_id,
        date,
        priority,
        status="PENDING"
    ):
        try:
            service = info.context["event_service"]
            event = service.create_event(
                name=name,
                description=description,
                event_type_id=event_type_id,
                zone_id=zone_id,
                date=date,
                priority=priority,
                status=status
            )
            return CreateEvent(
                event=event,
                success=True,
                message="Événement créé avec succès"
            )
        except Exception as e:
            return CreateEvent(
                event=None,
                success=False,
                message=f"Erreur: {str(e)}"
            )


class UpdateEvent(graphene.Mutation):
    """Mutation pour mettre à jour un événement"""
    
    class Arguments:
        event_id = graphene.String(required=True)
        name = graphene.String()
        description = graphene.String()
        event_type_id = graphene.String()
        zone_id = graphene.String()
        date = graphene.String()
        priority = graphene.String()
        status = graphene.String()
    
    event = graphene.Field(EventType)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(
        self,
        info,
        event_id,
        name=None,
        description=None,
        event_type_id=None,
        zone_id=None,
        date=None,
        priority=None,
        status=None
    ):
        try:
            service = info.context["event_service"]
            event = service.update_event(
                event_id=event_id,
                name=name,
                description=description,
                event_type_id=event_type_id,
                zone_id=zone_id,
                date=date,
                priority=priority,
                status=status
            )
            if event:
                return UpdateEvent(
                    event=event,
                    success=True,
                    message="Événement mis à jour avec succès"
                )
            return UpdateEvent(
                event=None,
                success=False,
                message="Événement introuvable"
            )
        except Exception as e:
            return UpdateEvent(
                event=None,
                success=False,
                message=f"Erreur: {str(e)}"
            )


class DeleteEvent(graphene.Mutation):
    """Mutation pour supprimer un événement"""
    
    class Arguments:
        event_id = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, event_id):
        try:
            service = info.context["event_service"]
            deleted = service.delete_event(event_id)
            if deleted:
                return DeleteEvent(
                    success=True,
                    message="Événement supprimé avec succès"
                )
            return DeleteEvent(
                success=False,
                message="Événement introuvable"
            )
        except Exception as e:
            return DeleteEvent(
                success=False,
                message=f"Erreur: {str(e)}"
            )


class Mutation(graphene.ObjectType):
    """Root Mutation"""
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()