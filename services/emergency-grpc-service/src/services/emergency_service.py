"""
Service métier pour la gestion des alertes d'urgence
Implémentation gRPC avec logique métier complète
"""
import grpc
from concurrent import futures
from typing import List, Dict
from datetime import datetime
from queue import Queue
import time

from src.models.alert import Alert, Location, AlertType, Priority, AlertStatus
from src.repository.alert_repository import AlertRepository
from src.validators.alert_validator import AlertValidator
from src.utils.logger import setup_logger

# Import des proto générés (à générer avec grpcio-tools)
from protos import emergency_pb2
from protos import emergency_pb2_grpc

# Logger
service_logger = setup_logger('emergency_service')


class EmergencyAlertService(emergency_pb2_grpc.EmergencyAlertServiceServicer):
    """
    Implémentation du service gRPC de gestion des alertes d'urgence
    """
    
    def __init__(self):
        self.repository = AlertRepository()
        self.validator = AlertValidator()
        self.subscribers: List[Dict] = []
        service_logger.info("EmergencyAlertService initialized")
    
    # ========================================================================
    # MAPPAGE PROTO <-> DOMAIN
    # ========================================================================
    
    def _map_alert_type_from_proto(self, proto_type: int) -> AlertType:
        """Convertit AlertType proto -> domain"""
        mapping = {
            1: AlertType.ACCIDENT,
            2: AlertType.FIRE,
            3: AlertType.AMBULANCE_REQUEST,
            4: AlertType.MEDICAL_EMERGENCY,
            5: AlertType.NATURAL_DISASTER,
            6: AlertType.SECURITY_THREAT,
            7: AlertType.PUBLIC_HEALTH
        }
        return mapping.get(proto_type, AlertType.ACCIDENT)
    
    def _map_alert_type_to_proto(self, alert_type: AlertType) -> int:
        """Convertit AlertType domain -> proto"""
        mapping = {
            AlertType.ACCIDENT: 1,
            AlertType.FIRE: 2,
            AlertType.AMBULANCE_REQUEST: 3,
            AlertType.MEDICAL_EMERGENCY: 4,
            AlertType.NATURAL_DISASTER: 5,
            AlertType.SECURITY_THREAT: 6,
            AlertType.PUBLIC_HEALTH: 7
        }
        return mapping.get(alert_type, 1)
    
    def _map_priority_from_proto(self, proto_priority: int) -> Priority:
        """Convertit Priority proto -> domain"""
        mapping = {1: Priority.LOW, 2: Priority.MEDIUM, 3: Priority.HIGH, 4: Priority.CRITICAL}
        return mapping.get(proto_priority, Priority.MEDIUM)
    
    def _map_priority_to_proto(self, priority: Priority) -> int:
        """Convertit Priority domain -> proto"""
        mapping = {Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 3, Priority.CRITICAL: 4}
        return mapping.get(priority, 2)
    
    def _map_status_from_proto(self, proto_status: int) -> AlertStatus:
        """Convertit AlertStatus proto -> domain"""
        mapping = {
            1: AlertStatus.PENDING,
            2: AlertStatus.IN_PROGRESS,
            3: AlertStatus.RESOLVED,
            4: AlertStatus.CANCELLED
        }
        return mapping.get(proto_status, AlertStatus.PENDING)
    
    def _map_status_to_proto(self, status: AlertStatus) -> int:
        """Convertit AlertStatus domain -> proto"""
        mapping = {
            AlertStatus.PENDING: 1,
            AlertStatus.IN_PROGRESS: 2,
            AlertStatus.RESOLVED: 3,
            AlertStatus.CANCELLED: 4
        }
        return mapping.get(status, 1)
    
    def _alert_to_response(self, alert: Alert) -> emergency_pb2.AlertResponse:
        """Convertit Alert domain -> AlertResponse proto"""
        return emergency_pb2.AlertResponse(
            alert_id=alert.alert_id,
            type=self._map_alert_type_to_proto(alert.alert_type),
            description=alert.description,
            location=emergency_pb2.Location(
                latitude=alert.location.latitude,
                longitude=alert.location.longitude,
                address=alert.location.address,
                city=alert.location.city,
                zone=alert.location.zone
            ),
            priority=self._map_priority_to_proto(alert.priority),
            status=self._map_status_to_proto(alert.status),
            reporter_name=alert.reporter_name,
            reporter_phone=alert.reporter_phone,
            affected_people=alert.affected_people,
            created_at=alert.created_at.isoformat(),
            updated_at=alert.updated_at.isoformat(),
            assigned_team=alert.assigned_team or "",
            notes=alert.notes or ""
        )
    
    # ========================================================================
    # RPC: CreateAlert
    # ========================================================================
    
    def CreateAlert(self, request, context):
        """
        Crée une nouvelle alerte d'urgence
        
        Processus:
        1. Validation complète des entrées
        2. Création de l'objet Alert
        3. Persistance dans le repository
        4. Notification des subscribers
        5. Retour de la réponse
        """
        service_logger.info(
            "CreateAlert request received",
            extra={
                "type": request.type,
                "zone": request.location.zone,
                "priority": request.priority
            }
        )
        
        try:
            # Validation des entrées
            self.validator.validate_description(request.description)
            self.validator.validate_phone(request.reporter_phone)
            self.validator.validate_location(
                request.location.latitude,
                request.location.longitude,
                request.location.address,
                request.location.city,
                request.location.zone
            )
            self.validator.validate_reporter_name(request.reporter_name)
            self.validator.validate_affected_people(request.affected_people)
            
            # Transformation proto -> domain
            location = Location(
                latitude=request.location.latitude,
                longitude=request.location.longitude,
                address=request.location.address,
                city=request.location.city,
                zone=request.location.zone
            )
            
            alert = Alert(
                alert_type=self._map_alert_type_from_proto(request.type),
                description=request.description,
                location=location,
                priority=self._map_priority_from_proto(request.priority),
                reporter_name=request.reporter_name,
                reporter_phone=request.reporter_phone,
                affected_people=request.affected_people
            )
            
            # Persistance
            created_alert = self.repository.create(alert)
            
            # Notification des subscribers
            self._notify_subscribers(created_alert)
            
            service_logger.info(
                f"Alert created successfully: {created_alert.alert_id}",
                extra={"alert_id": created_alert.alert_id}
            )
            
            return self._alert_to_response(created_alert)
        
        except ValueError as e:
            service_logger.error(f"Validation error: {str(e)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return emergency_pb2.AlertResponse()
        
        except Exception as e:
            service_logger.error(f"Internal error: {str(e)}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            return emergency_pb2.AlertResponse()
    
    # ========================================================================
    # RPC: GetActiveAlerts
    # ========================================================================
    
    def GetActiveAlerts(self, request, context):
        """
        Récupère les alertes actives d'une zone géographique
        
        Filtres:
        - Zone (obligatoire)
        - Type d'alerte (optionnel)
        - Priorité minimale (optionnel)
        """
        service_logger.info(
            f"GetActiveAlerts request for zone: {request.zone}",
            extra={"zone": request.zone}
        )
        
        try:
            # Validation
            if not request.zone or not request.zone.strip():
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Zone cannot be empty")
                return emergency_pb2.AlertListResponse()
            
            # Extraction des filtres
            alert_type = self._map_alert_type_from_proto(request.type) if request.type else None
            min_priority = self._map_priority_from_proto(request.min_priority) if request.min_priority else None
            
            # Récupération
            alerts = self.repository.get_active_by_zone(
                zone=request.zone,
                alert_type=alert_type,
                min_priority=min_priority
            )
            
            service_logger.info(f"Found {len(alerts)} active alerts in zone {request.zone}")
            
            # Construction de la réponse
            return emergency_pb2.AlertListResponse(
                alerts=[self._alert_to_response(alert) for alert in alerts],
                total_count=len(alerts)
            )
        
        except Exception as e:
            service_logger.error(f"Error getting active alerts: {str(e)}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return emergency_pb2.AlertListResponse()
    
    # ========================================================================
    # RPC: UpdateAlertStatus
    # ========================================================================
    
    def UpdateAlertStatus(self, request, context):
        """
        Met à jour le statut d'une alerte et assigne une équipe
        
        Transitions possibles:
        - PENDING -> IN_PROGRESS
        - PENDING -> CANCELLED
        - IN_PROGRESS -> RESOLVED
        """
        service_logger.info(
            f"UpdateAlertStatus request for alert: {request.alert_id}",
            extra={
                "alert_id": request.alert_id,
                "new_status": request.new_status
            }
        )
        
        try:
            # Validation
            if not request.alert_id or not request.alert_id.strip():
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Alert ID cannot be empty")
                return emergency_pb2.AlertResponse()
            
            # Récupération
            alert = self.repository.get_by_id(request.alert_id)
            if not alert:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Alert not found: {request.alert_id}")
                return emergency_pb2.AlertResponse()
            
            # Mise à jour
            new_status = self._map_status_from_proto(request.new_status)
            alert.update_status(
                new_status=new_status,
                assigned_team=request.assigned_team if request.assigned_team else None,
                notes=request.notes if request.notes else None
            )
            
            # Persistance
            updated_alert = self.repository.update(alert)
            
            # Notification des subscribers
            self._notify_subscribers(updated_alert)
            
            service_logger.info(
                f"Alert status updated: {updated_alert.alert_id} -> {updated_alert.status.value}"
            )
            
            return self._alert_to_response(updated_alert)
        
        except Exception as e:
            service_logger.error(f"Error updating alert status: {str(e)}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return emergency_pb2.AlertResponse()
    
    # ========================================================================
    # RPC: GetAlertHistory
    # ========================================================================
    
    def GetAlertHistory(self, request, context):
        """
        Consulte l'historique des alertes avec statistiques
        
        Filtres:
        - Zone (optionnel)
        - Type (optionnel)
        - Période: start_date -> end_date (optionnel)
        - Limite de résultats (défaut: 100)
        """
        service_logger.info("GetAlertHistory request received")
        
        try:
            # Conversion timestamps
            start_date = datetime.fromtimestamp(request.start_date) if request.start_date else None
            end_date = datetime.fromtimestamp(request.end_date) if request.end_date else None
            
            # Récupération historique
            alert_type = self._map_alert_type_from_proto(request.type) if request.type else None
            limit = request.limit if request.limit > 0 else 100
            
            alerts = self.repository.get_history(
                zone=request.zone if request.zone else None,
                alert_type=alert_type,
                start_date=start_date,
                end_date=end_date,
                limit=limit
            )
            
            # Génération des statistiques
            statistics = self.repository.get_statistics(
                zone=request.zone if request.zone else None,
                start_date=start_date,
                end_date=end_date
            )
            
            service_logger.info(
                f"History retrieved: {len(alerts)} alerts",
                extra={"total": statistics.get("total", 0)}
            )
            
            return emergency_pb2.AlertHistoryResponse(
                alerts=[self._alert_to_response(alert) for alert in alerts],
                total_count=len(alerts),
                statistics=statistics
            )
        
        except Exception as e:
            service_logger.error(f"Error getting alert history: {str(e)}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return emergency_pb2.AlertHistoryResponse()
    
    # ========================================================================
    # RPC: SubscribeAlerts (Streaming)
    # ========================================================================
    
    def SubscribeAlerts(self, request, context):
        """
        Stream continu des alertes correspondant aux critères
        
        Fonctionnement:
        1. Créer un subscriber avec queue FIFO
        2. Envoyer les alertes actives existantes
        3. Boucle d'écoute continue pour nouvelles alertes
        4. Cleanup à la déconnexion
        """
        service_logger.info(
            "New subscriber connected",
            extra={
                "zones": list(request.zones),
                "min_priority": request.min_priority
            }
        )
        
        # Créer le subscriber
        subscriber = {
            "zones": list(request.zones),
            "types": [self._map_alert_type_from_proto(t) for t in request.types] if request.types else [],
            "min_priority": self._map_priority_from_proto(request.min_priority) if request.min_priority else Priority.LOW,
            "queue": Queue()
        }
        
        self.subscribers.append(subscriber)
        
        try:
            # Envoyer les alertes actives existantes
            for zone in request.zones:
                active_alerts = self.repository.get_active_by_zone(zone)
                for alert in active_alerts:
                    if self._matches_subscription(alert, subscriber):
                        yield self._alert_to_response(alert)
            
            # Boucle d'écoute continue
            while context.is_active():
                try:
                    # Attendre une nouvelle alerte (timeout 1s)
                    alert = subscriber["queue"].get(timeout=1.0)
                    yield self._alert_to_response(alert)
                except:
                    # Timeout, continuer la boucle
                    continue
        
        finally:
            # Cleanup à la déconnexion
            self.subscribers.remove(subscriber)
            service_logger.info("Subscriber disconnected")
    
    # ========================================================================
    # RPC: HealthCheck
    # ========================================================================
    
    def HealthCheck(self, request, context):
        """Health check du service"""
        try:
            all_alerts = self.repository.get_all()
            active_count = len([a for a in all_alerts if a.status in [AlertStatus.PENDING, AlertStatus.IN_PROGRESS]])
            
            return emergency_pb2.HealthCheckResponse(
                status="healthy",
                version="1.0.0",
                active_alerts=active_count,
                subscribers=len(self.subscribers)
            )
        except Exception as e:
            service_logger.error(f"Health check failed: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return emergency_pb2.HealthCheckResponse(status="unhealthy", version="1.0.0")
    
    # ========================================================================
    # MÉTHODES UTILITAIRES
    # ========================================================================
    
    def _notify_subscribers(self, alert: Alert):
        """Notifie tous les subscribers intéressés par cette alerte"""
        for subscriber in self.subscribers:
            if self._matches_subscription(alert, subscriber):
                subscriber["queue"].put(alert)
    
    def _matches_subscription(self, alert: Alert, subscriber: Dict) -> bool:
        """Vérifie si une alerte correspond aux critères d'un subscriber"""
        # Vérifier la zone
        if alert.location.zone not in subscriber["zones"]:
            return False
        
        # Vérifier le type (si spécifié)
        if subscriber["types"] and alert.alert_type not in subscriber["types"]:
            return False
        
        # Vérifier la priorité minimale
        if alert.priority.value < subscriber["min_priority"].value:
            return False
        
        return True
