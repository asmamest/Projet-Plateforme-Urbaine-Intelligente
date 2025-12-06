"""
Exemple de client gRPC pour tester le service
"""
import grpc
from protos import emergency_pb2, emergency_pb2_grpc


def create_alert_example():
    """Exemple : Créer une alerte"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)
    
    request = emergency_pb2.AlertRequest(
        type=emergency_pb2.FIRE,
        description="Incendie dans un immeuble résidentiel, 3ème étage",
        location=emergency_pb2.Location(
            latitude=48.8566,
            longitude=2.3522,
            address="25 Rue de la République",
            city="Paris",
            zone="Zone Centre"
        ),
        priority=emergency_pb2.CRITICAL,
        reporter_name="Marie Dubois",
        reporter_phone="+33612345678",
        affected_people=8
    )
    
    try:
        response = stub.CreateAlert(request)
        print(f"✅ Alerte créée: {response.alert_id}")
        print(f"   Statut: {emergency_pb2.AlertStatus.Name(response.status)}")
        print(f"   Priorité: {emergency_pb2.Priority.Name(response.priority)}")
    except grpc.RpcError as e:
        print(f"❌ Erreur: {e.code()}: {e.details()}")


def get_active_alerts_example():
    """Exemple : Récupérer alertes actives"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)
    
    request = emergency_pb2.ZoneRequest(
        zone="Zone Centre",
        min_priority=emergency_pb2.HIGH
    )
    
    try:
        response = stub.GetActiveAlerts(request)
        print(f"📋 {response.total_count} alertes actives trouvées:")
        
        for alert in response.alerts:
            print(f"\n   ID: {alert.alert_id}")
            print(f"   Type: {emergency_pb2.AlertType.Name(alert.type)}")
            print(f"   Description: {alert.description[:50]}...")
            print(f"   Priorité: {emergency_pb2.Priority.Name(alert.priority)}")
    except grpc.RpcError as e:
        print(f"❌ Erreur: {e.code()}: {e.details()}")


def update_alert_status_example(alert_id):
    """Exemple : Mettre à jour le statut"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)
    
    request = emergency_pb2.StatusUpdateRequest(
        alert_id=alert_id,
        new_status=emergency_pb2.IN_PROGRESS,
        assigned_team="Pompiers Caserne 5",
        notes="Équipe de 6 pompiers en route, ETA 8 minutes"
    )
    
    try:
        response = stub.UpdateAlertStatus(request)
        print(f"✅ Alerte mise à jour: {response.alert_id}")
        print(f"   Nouveau statut: {emergency_pb2.AlertStatus.Name(response.status)}")
        print(f"   Équipe: {response.assigned_team}")
    except grpc.RpcError as e:
        print(f"❌ Erreur: {e.code()}: {e.details()}")


def subscribe_alerts_example():
    """Exemple : S'abonner aux alertes en streaming"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)
    
    request = emergency_pb2.SubscribeRequest(
        zones=["Zone Centre", "Zone Nord"],
        types=[emergency_pb2.FIRE, emergency_pb2.MEDICAL_EMERGENCY],
        min_priority=emergency_pb2.HIGH
    )
    
    print("🔄 Streaming des alertes en temps réel...")
    print("   (Appuyez sur Ctrl+C pour arrêter)\n")
    
    try:
        for alert in stub.SubscribeAlerts(request):
            print(f"🚨 NOUVELLE ALERTE:")
            print(f"   ID: {alert.alert_id}")
            print(f"   Type: {emergency_pb2.AlertType.Name(alert.type)}")
            print(f"   Zone: {alert.location.zone}")
            print(f"   Priorité: {emergency_pb2.Priority.Name(alert.priority)}")
            print(f"   Description: {alert.description[:80]}...")
            print()
    except KeyboardInterrupt:
        print("\n✋ Streaming arrêté")
    except grpc.RpcError as e:
        print(f"❌ Erreur: {e.code()}: {e.details()}")


def health_check_example():
    """Exemple : Health check"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)
    
    request = emergency_pb2.HealthCheckRequest()
    
    try:
        response = stub.HealthCheck(request)
        print(f"💚 Service: {response.status}")
        print(f"   Version: {response.version}")
        print(f"   Alertes actives: {response.active_alerts}")
        print(f"   Subscribers: {response.subscribers}")
    except grpc.RpcError as e:
        print(f"❌ Service unhealthy: {e.code()}")


if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Emergency Alert gRPC Client Examples")
    print("=" * 60)
    
    # 1. Health check
    print("\n1️⃣ Health Check:")
    health_check_example()
    
    # 2. Créer une alerte
    print("\n2️⃣ Créer une alerte:")
    create_alert_example()
    
    # 3. Récupérer alertes actives
    print("\n3️⃣ Récupérer alertes actives:")
    get_active_alerts_example()
    
    # 4. S'abonner (streaming)
    # Décommenter pour tester le streaming
    print("\n4️⃣ S'abonner aux alertes:")
    subscribe_alerts_example()