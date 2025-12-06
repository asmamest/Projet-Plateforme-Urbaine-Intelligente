# Emergency Alert Service - gRPC Microservice

Microservice gRPC professionnel pour la gestion des alertes d'urgence et de santé publique en temps réel.

## 📋 Table des matières

- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [API gRPC](#api-grpc)
- [Exemples](#exemples)
- [Tests](#tests)
- [Docker](#docker)
- [Intégrations](#intégrations)

## 🏗️ Architecture

```
emergency-grpc-service/
├── protos/
│   └── emergency.proto          # Définition Protocol Buffers
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── alert.py             # Alert, Location, Enums
│   ├── repository/
│   │   ├── __init__.py
│   │   └── alert_repository.py  # Repository pattern
│   ├── services/
│   │   ├── __init__.py
│   │   └── emergency_service.py # Service gRPC
│   ├── validators/
│   │   ├── __init__.py
│   │   └── alert_validator.py   # Validation stricte
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py            # Logging JSON
│   └── server.py                # Serveur gRPC
├── tests/
│   ├── test_repository.py
│   └── test_validator.py
├── client_example.py            # Exemples client
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── build_protos.sh
└── README.md
```

## 📦 Installation

### Prérequis

- Python 3.11+
- pip
- grpcio-tools

### Installation locale

```bash
# Cloner le projet
cd emergency-grpc-service

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Générer les fichiers Protocol Buffers
chmod +x build_protos.sh
./build_protos.sh

# Ou manuellement:
python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./protos \
    --grpc_python_out=./protos \
    ./protos/emergency.proto

# Lancer le serveur
python -m src.server
```

Le service sera accessible sur `localhost:50051`

## 🚀 Utilisation

### Démarrage rapide

```bash
# Lancer le serveur
python -m src.server

# Dans un autre terminal, tester avec le client
python client_example.py
```

## 📘 API gRPC

### RPC Methods

#### 1. CreateAlert

Crée une nouvelle alerte d'urgence.

```protobuf
rpc CreateAlert(AlertRequest) returns (AlertResponse);
```

**Request:**

```json
{
  "type": "FIRE",
  "description": "Incendie dans un immeuble résidentiel",
  "location": {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "address": "123 Rue de Rivoli",
    "city": "Paris",
    "zone": "Zone Centre"
  },
  "priority": "CRITICAL",
  "reporter_name": "Jean Dupont",
  "reporter_phone": "+33612345678",
  "affected_people": 10
}
```

**Response:**

```json
{
  "alert_id": "ALERT-A3F2E1B9C4D8",
  "status": "PENDING",
  "created_at": "2025-12-06T10:30:00Z",
  ...
}
```

#### 2. GetActiveAlerts

Récupère les alertes actives d'une zone.

```protobuf
rpc GetActiveAlerts(ZoneRequest) returns (AlertListResponse);
```

**Request:**

```json
{
  "zone": "Zone Centre",
  "type": "FIRE", // Optionnel
  "min_priority": "HIGH" // Optionnel
}
```

**Response:**

```json
{
  "alerts": [...],
  "total_count": 5
}
```

#### 3. UpdateAlertStatus

Met à jour le statut d'une alerte.

```protobuf
rpc UpdateAlertStatus(StatusUpdateRequest) returns (AlertResponse);
```

**Request:**

```json
{
  "alert_id": "ALERT-A3F2E1B9C4D8",
  "new_status": "IN_PROGRESS",
  "assigned_team": "Pompiers Caserne 5",
  "notes": "Équipe en route, ETA 8 minutes"
}
```

#### 4. GetAlertHistory

Consulte l'historique avec statistiques.

```protobuf
rpc GetAlertHistory(HistoryRequest) returns (AlertHistoryResponse);
```

**Request:**

```json
{
  "zone": "Zone Nord",
  "type": "ACCIDENT",
  "start_date": 1733443200, // Timestamp Unix
  "end_date": 1733529600,
  "limit": 100
}
```

**Response:**

```json
{
  "alerts": [...],
  "total_count": 45,
  "statistics": {
    "total": 45,
    "pending": 3,
    "in_progress": 7,
    "resolved": 32,
    "cancelled": 3,
    "type_accident": 15,
    "type_fire": 10,
    ...
  }
}
```

#### 5. SubscribeAlerts (Streaming)

Stream temps réel des alertes.

```protobuf
rpc SubscribeAlerts(SubscribeRequest) returns (stream AlertResponse);
```

**Request:**

```json
{
  "zones": ["Zone Centre", "Zone Nord"],
  "types": ["FIRE", "MEDICAL_EMERGENCY"],
  "min_priority": "HIGH"
}
```

**Response:** Stream continu d'`AlertResponse`

#### 6. HealthCheck

Vérifie la santé du service.

```protobuf
rpc HealthCheck(HealthCheckRequest) returns (HealthCheckResponse);
```

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "active_alerts": 12,
  "subscribers": 3
}
```

### Types d'alertes

| Type                | Description                        |
| ------------------- | ---------------------------------- |
| `ACCIDENT`          | Accident de la route ou industriel |
| `FIRE`              | Incendie                           |
| `AMBULANCE_REQUEST` | Demande d'ambulance                |
| `MEDICAL_EMERGENCY` | Urgence médicale critique          |
| `NATURAL_DISASTER`  | Catastrophe naturelle              |
| `SECURITY_THREAT`   | Menace sécuritaire                 |
| `PUBLIC_HEALTH`     | Crise de santé publique            |

### Priorités

| Priorité   | Temps de réponse | Description             |
| ---------- | ---------------- | ----------------------- |
| `LOW`      | < 30 minutes     | Pas de danger immédiat  |
| `MEDIUM`   | < 15 minutes     | Situation stable        |
| `HIGH`     | < 8 minutes      | Danger potentiel        |
| `CRITICAL` | < 5 minutes      | Danger de mort imminent |

### Statuts

| Statut        | Description              |
| ------------- | ------------------------ |
| `PENDING`     | En attente d'assignation |
| `IN_PROGRESS` | Intervention en cours    |
| `RESOLVED`    | Résolue                  |
| `CANCELLED`   | Annulée                  |

## 💡 Exemples

### Python Client

```python
import grpc
from protos import emergency_pb2, emergency_pb2_grpc

# Connexion
channel = grpc.insecure_channel('localhost:50051')
stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)

# Créer une alerte
request = emergency_pb2.AlertRequest(
    type=emergency_pb2.FIRE,
    description="Incendie appartement 3ème étage",
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
    affected_people=5
)

response = stub.CreateAlert(request)
print(f"Alert created: {response.alert_id}")

# Récupérer alertes actives
zone_request = emergency_pb2.ZoneRequest(zone="Zone Centre")
active_alerts = stub.GetActiveAlerts(zone_request)

for alert in active_alerts.alerts:
    print(f"{alert.alert_id}: {alert.description}")

# Streaming temps réel
subscribe_request = emergency_pb2.SubscribeRequest(
    zones=["Zone Centre"],
    min_priority=emergency_pb2.HIGH
)

for alert in stub.SubscribeAlerts(subscribe_request):
    print(f"New alert: {alert.alert_id}")
```

### Node.js Client

```javascript
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const packageDefinition = protoLoader.loadSync("protos/emergency.proto");
const proto = grpc.loadPackageDefinition(packageDefinition).emergency;

const client = new proto.EmergencyAlertService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

// Créer une alerte
client.CreateAlert(
  {
    type: "FIRE",
    description: "Incendie dans un immeuble",
    location: {
      latitude: 48.8566,
      longitude: 2.3522,
      address: "123 Rue Test",
      city: "Paris",
      zone: "Zone Centre",
    },
    priority: "CRITICAL",
    reporter_name: "Test User",
    reporter_phone: "+33612345678",
    affected_people: 8,
  },
  (error, response) => {
    if (error) {
      console.error("Error:", error);
    } else {
      console.log("Alert created:", response.alert_id);
    }
  }
);

// Streaming
const call = client.SubscribeAlerts({
  zones: ["Zone Centre"],
  min_priority: "HIGH",
});

call.on("data", (alert) => {
  console.log("New alert:", alert.alert_id);
});
```

### Go Client

```go
package main

import (
    "context"
    "log"
    "google.golang.org/grpc"
    pb "path/to/emergency"
)

func main() {
    conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    client := pb.NewEmergencyAlertServiceClient(conn)

    // Créer une alerte
    response, err := client.CreateAlert(context.Background(), &pb.AlertRequest{
        Type: pb.AlertType_FIRE,
        Description: "Incendie immeuble",
        Location: &pb.Location{
            Latitude: 48.8566,
            Longitude: 2.3522,
            Address: "123 Rue Test",
            City: "Paris",
            Zone: "Zone Centre",
        },
        Priority: pb.Priority_CRITICAL,
        ReporterName: "Test User",
        ReporterPhone: "+33612345678",
        AffectedPeople: 5,
    })

    if err != nil {
        log.Fatal(err)
    }

    log.Printf("Alert created: %s", response.AlertId)
}
```

## 🧪 Tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_repository.py
pytest tests/test_validator.py

# Tests avec sortie détaillée
pytest -v
```

## 🐳 Docker

### Build et run

```bash
# Build l'image
docker build -t emergency-grpc-service .

# Lancer le conteneur
docker run -d \
  --name emergency-service \
  -p 50051:50051 \
  emergency-grpc-service

# Vérifier les logs
docker logs emergency-service

# Health check
docker exec emergency-service \
  python -c "import grpc; from protos import emergency_pb2, emergency_pb2_grpc; \
  channel = grpc.insecure_channel('localhost:50051'); \
  stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel); \
  print(stub.HealthCheck(emergency_pb2.HealthCheckRequest()))"

# Arrêter
docker stop emergency-service
```

### Docker Compose

```bash
# Lancer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

## 🔗 Intégrations

### API Gateway REST (FastAPI)

Le service peut être exposé via une API REST:

```python
from fastapi import FastAPI
import grpc
from protos import emergency_pb2, emergency_pb2_grpc

app = FastAPI()

@app.post("/api/v1/alerts")
async def create_alert(alert: AlertCreate):
    channel = grpc.insecure_channel('localhost:50051')
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel)

    request = emergency_pb2.AlertRequest(...)
    response = stub.CreateAlert(request)

    return {"alert_id": response.alert_id}
```

### GraphQL (Strawberry)

```python
import strawberry
import grpc

@strawberry.type
class Alert:
    id: str
    type: str
    description: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_alert(self, ...) -> Alert:
        # Appel gRPC
        ...
```

### Message Broker (RabbitMQ/Kafka)

Publier des événements lors des changements:

```python
import pika

def publish_alert_created(alert):
    connection = pika.BlockingConnection(...)
    channel = connection.channel()

    channel.basic_publish(
        exchange='emergency.alerts',
        routing_key=f'alert.created.{alert.type}',
        body=json.dumps(alert.to_dict())
    )
```

## 📊 Monitoring

### Prometheus Métriques

```python
from prometheus_client import Counter, Histogram

alerts_created = Counter('alerts_created_total', 'Total alerts created')
request_duration = Histogram('grpc_request_duration_seconds', 'Request duration')

# Dans le service
alerts_created.inc()
with request_duration.time():
    # ... traitement
```

### Grafana Dashboard

Panneaux recommandés:

- Total d'alertes par type
- Temps de réponse moyen
- Alertes actives par zone
- Distribution des priorités

## 🚀 Production

### Variables d'environnement

```bash
GRPC_PORT=50051
LOG_LEVEL=INFO
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emergency-grpc
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: emergency-grpc
          image: emergency-grpc-service:latest
          ports:
            - containerPort: 50051
          env:
            - name: GRPC_PORT
              value: "50051"
```

## 📝 License

MIT

## 👥 Auteurs

Smart City Platform Team

---

**Version**: 1.0.0  
**Port gRPC**: 50051  
**Documentation**: [Protocol Buffers](https://protobuf.dev/)
"""
