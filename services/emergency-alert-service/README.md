# 🚨 Emergency Alert Service - Microservice gRPC

Microservice gRPC professionnel pour la gestion des alertes d'urgence et de santé publique en temps réel.

## 📋 Table des matières

- [Caractéristiques](#caractéristiques)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [API gRPC](#api-grpc)
- [Docker](#docker)
- [Tests](#tests)
- [Intégration](#intégration)
- [Sécurité](#sécurité)

## ✨ Caractéristiques

### Fonctionnalités métier

- ✅ **Création d'alertes** : Accidents, incendies, urgences médicales, catastrophes naturelles
- ✅ **Gestion en temps réel** : Suivi des alertes actives par zone géographique
- ✅ **Mises à jour de statut** : Pending → In Progress → Resolved
- ✅ **Notifications instantanées** : Streaming gRPC pour alertes temps réel
- ✅ **Historique & Analytics** : Consultation des alertes passées avec statistiques

### Fonctionnalités techniques

- ✅ **Validation robuste** : Validation complète des entrées avec messages d'erreur clairs
- ✅ **Logging JSON** : Traçabilité complète de toutes les opérations
- ✅ **Repository Pattern** : Architecture prête pour intégration DB (PostgreSQL, MongoDB, etc.)
- ✅ **Thread-safe** : Gestion sécurisée des accès concurrents
- ✅ **Error Handling** : Gestion propre des erreurs avec codes gRPC appropriés
- ✅ **Docker ready** : Containerisation complète avec Docker Compose
- ✅ **Streaming bidirectionnel** : Support complet du streaming gRPC

## 🏗️ Architecture

```
emergency-alert-service/
├── proto/                      # Définitions Protocol Buffers
│   ├── emergency.proto         # Schéma gRPC
│   ├── emergency_pb2.py        # Généré automatiquement
│   └── emergency_pb2_grpc.py   # Généré automatiquement
│
├── src/
│   ├── models/                 # Modèles de domaine
│   │   └── alert.py            # Classes Alert, Location, Enums
│   │
│   ├── repository/             # Couche de persistance
│   │   └── alert_repository.py # Repository pattern (prêt pour DB)
│   │
│   ├── services/               # Logique métier
│   │   └── emergency_service.py # Implémentation gRPC
│   │
│   ├── validators/             # Validation des données
│   │   └── alert_validator.py  # Validateurs d'entrée
│   │
│   ├── utils/                  # Utilitaires
│   │   └── logger.py           # Configuration logging
│   │
│   ├── server.py               # Serveur gRPC
│   └── client_examples.py      # Exemples d'utilisation
│
├── tests/                      # Tests unitaires
├── Dockerfile                  # Image Docker
├── docker-compose.yml          # Orchestration
└── requirements.txt            # Dépendances Python
```

### Principes architecturaux

- **Separation of Concerns** : Chaque couche a sa responsabilité
- **Dependency Inversion** : Repository abstrait pour faciliter le swap de DB
- **Single Responsibility** : Classes focalisées sur une seule tâche
- **Thread-Safety** : Verrous pour opérations concurrentes
- **Observability** : Logging structuré en JSON

## 📦 Prérequis

- **Python** : 3.9+ (recommandé 3.11)
- **pip** : Gestionnaire de paquets Python
- **Docker** : (optionnel) Pour containerisation
- **grpcio-tools** : Génération des stubs Protocol Buffers

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <repo-url>
cd emergency-alert-service
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Générer les stubs gRPC

```bash
chmod +x generate_proto.sh
./generate_proto.sh
```

✅ Vous êtes prêt !

## 🎯 Utilisation

### Lancer le serveur

```bash
chmod +x run_server.sh
./run_server.sh
```

Le serveur démarre sur `localhost:50051` 🚀

### Tester avec le client d'exemples

Dans un autre terminal :

```bash
chmod +x run_client.sh
./run_client.sh
```

Cela exécutera tous les exemples d'utilisation du service.

## 📡 API gRPC

### Méthodes disponibles

#### 1. CreateAlert

Crée une nouvelle alerte d'urgence.

```protobuf
rpc CreateAlert(AlertRequest) returns (AlertResponse);
```

**Exemple Python :**

```python
import grpc
from proto import emergency_pb2, emergency_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)

request = emergency_pb2.AlertRequest(
    type=emergency_pb2.FIRE,
    description="Incendie dans un immeuble résidentiel",
    location=emergency_pb2.Location(
        latitude=48.8566,
        longitude=2.3522,
        address="123 Rue de la Paix",
        city="Paris",
        zone="Zone Centre"
    ),
    priority=emergency_pb2.CRITICAL,
    reporter_name="Marie Martin",
    reporter_phone="+33612345678",
    affected_people=15
)

response = stub.CreateAlert(request)
print(f"Alerte créée: {response.alert_id}")
```

#### 2. GetActiveAlerts

Récupère les alertes actives d'une zone.

```protobuf
rpc GetActiveAlerts(ZoneRequest) returns (AlertListResponse);
```

**Exemple Python :**

```python
request = emergency_pb2.ZoneRequest(
    zone="Zone Centre",
    type=emergency_pb2.FIRE,  # Optionnel
    min_priority=emergency_pb2.HIGH  # Optionnel
)

response = stub.GetActiveAlerts(request)
print(f"{response.total_count} alertes actives")
for alert in response.alerts:
    print(f"- {alert.alert_id}: {alert.description}")
```

#### 3. UpdateAlertStatus

Met à jour le statut d'une alerte.

```protobuf
rpc UpdateAlertStatus(UpdateStatusRequest) returns (AlertResponse);
```

**Exemple Python :**

```python
request = emergency_pb2.UpdateStatusRequest(
    alert_id="ALERT-ABC123",
    new_status=emergency_pb2.IN_PROGRESS,
    assigned_team="Pompiers Caserne 5",
    notes="Équipe de 8 pompiers sur place"
)

response = stub.UpdateAlertStatus(request)
print(f"Statut mis à jour: {emergency_pb2.AlertStatus.Name(response.status)}")
```

#### 4. GetAlertHistory

Consulte l'historique des alertes avec statistiques.

```protobuf
rpc GetAlertHistory(HistoryRequest) returns (AlertHistoryResponse);
```

**Exemple Python :**

```python
import time

request = emergency_pb2.HistoryRequest(
    zone="Zone Centre",  # Optionnel
    type=emergency_pb2.FIRE,  # Optionnel
    start_date=int(time.time()) - 86400,  # Dernières 24h
    end_date=int(time.time()),
    limit=50
)

response = stub.GetAlertHistory(request)
print(f"Historique: {response.total_count} alertes")
print(f"Statistiques: {dict(response.statistics)}")
```

#### 5. SubscribeAlerts (Streaming)

S'abonne aux alertes en temps réel.

```protobuf
rpc SubscribeAlerts(SubscribeRequest) returns (stream AlertResponse);
```

**Exemple Python :**

```python
request = emergency_pb2.SubscribeRequest(
    zones=["Zone Centre", "Zone Nord"],
    types=[emergency_pb2.FIRE, emergency_pb2.ACCIDENT],
    min_priority=emergency_pb2.HIGH
)

# Stream continu
for alert in stub.SubscribeAlerts(request):
    print(f"🔔 Nouvelle alerte: {alert.alert_id}")
    print(f"   Type: {emergency_pb2.AlertType.Name(alert.type)}")
    print(f"   Zone: {alert.location.zone}")
```

### Types de données

#### AlertType (Types d'urgence)

- `ACCIDENT` : Accident de la route
- `FIRE` : Incendie
- `AMBULANCE_REQUEST` : Demande d'ambulance
- `MEDICAL_EMERGENCY` : Urgence médicale
- `NATURAL_DISASTER` : Catastrophe naturelle
- `SECURITY_THREAT` : Menace sécuritaire
- `PUBLIC_HEALTH` : Santé publique

#### AlertStatus (Statuts)

- `PENDING` : En attente
- `IN_PROGRESS` : En intervention
- `RESOLVED` : Résolue
- `CANCELLED` : Annulée

#### Priority (Priorités)

- `LOW` : Faible
- `MEDIUM` : Moyenne
- `HIGH` : Haute
- `CRITICAL` : Critique

## 🐳 Docker

### Build et lancement avec Docker Compose

```bash
docker-compose up --build
```

Le service sera accessible sur `localhost:50051`

### Arrêt

```bash
docker-compose down
```

### Build manuel

```bash
docker build -t emergency-alert-service .
docker run -p 50051:50051 emergency-alert-service
```

## 🧪 Tests

### Lancer les tests unitaires

```bash
pytest tests/ -v
```

### Tester avec grpcurl

```bash
# Lister les services
grpcurl -plaintext localhost:50051 list

# Créer une alerte
grpcurl -plaintext -d '{
  "type": 2,
  "description": "Test incendie",
  "location": {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "address": "Test",
    "city": "Paris",
    "zone": "Zone Test"
  },
  "priority": 4,
  "reporter_name": "Test User",
  "reporter_phone": "+33612345678",
  "affected_people": 5
}' localhost:50051 emergency.EmergencyAlertService/CreateAlert
```

## 🔌 Intégration

### Intégration avec une base de données

Le `AlertRepository` est conçu pour être facilement remplacé :

```python
# src/repository/alert_repository_postgres.py
from sqlalchemy import create_engine
from src.repository.alert_repository import AlertRepository

class PostgresAlertRepository(AlertRepository):
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        # Implémentez les méthodes avec SQLAlchemy

    def create(self, alert):
        # Logique PostgreSQL
        pass
```

Puis dans `src/services/emergency_service.py` :

```python
def __init__(self):
    # self.repository = AlertRepository()  # Ancien
    self.repository = PostgresAlertRepository(os.getenv("DATABASE_URL"))
```

### Intégration REST API Gateway

```python
# api_gateway.py (exemple avec FastAPI)
from fastapi import FastAPI
import grpc
from proto import emergency_pb2, emergency_pb2_grpc

app = FastAPI()

@app.post("/alerts")
async def create_alert(alert_data: dict):
    channel = grpc.insecure_channel('emergency-service:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)

    request = emergency_pb2.AlertRequest(**alert_data)
    response = stub.CreateAlert(request)

    return {"alert_id": response.alert_id}
```

### Intégration Message Broker (RabbitMQ)

```python
# src/integrations/rabbitmq_publisher.py
import pika
import json

class AlertPublisher:
    def __init__(self, connection_url):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_url)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare('alerts', 'topic')

    def publish_alert(self, alert):
        routing_key = f"alert.{alert.alert_type.value}.{alert.priority.value}"
        message = json.dumps(alert.to_dict())

        self.channel.basic_publish(
            exchange='alerts',
            routing_key=routing_key,
            body=message
        )
```

## 🔐 Sécurité

### Pour production, implémentez :

1. **TLS/SSL** : Chiffrement des communications

```python
# Serveur avec TLS
server_credentials = grpc.ssl_server_credentials(
    [(private_key, certificate_chain)]
)
server.add_secure_port('[::]:50051', server_credentials)
```

2. **Authentification** : Token JWT ou mTLS

```python
# Intercepteur d'authentification
class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        # Vérifier le token
        metadata = dict(handler_call_details.invocation_metadata)
        token = metadata.get('authorization')

        if not self.validate_token(token):
            return grpc.unary_unary_rpc_method_handler(
                lambda request, context: context.abort(
                    grpc.StatusCode.UNAUTHENTICATED,
                    'Invalid token'
                )
            )

        return continuation(handler_call_details)
```

3. **Rate Limiting** : Limitation des requêtes

4. **Input Sanitization** : Validation stricte (déjà implémentée)

## 📊 Monitoring

### Métriques recommandées

- Nombre d'alertes créées par minute
- Temps de réponse moyen par méthode
- Taux d'erreur
- Nombre de subscribers actifs
- Distribution des types d'alertes
- Distribution des priorités

### Intégration Prometheus (exemple)

```python
from prometheus_client import Counter, Histogram

alerts_created = Counter('alerts_created_total', 'Total alerts created')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@request_duration.time()
def CreateAlert(self, request, context):
    alerts_created.inc()
    # ... reste du code
```

## 🤝 Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

---

**Note importante** : Ce service utilise actuellement un stockage en mémoire pour les données (mockées). Pour une utilisation en production, intégrez une vraie base de données (PostgreSQL, MongoDB, etc.) via le `AlertRepository`.
