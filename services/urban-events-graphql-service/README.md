# Urban Events GraphQL Service

Microservice GraphQL professionnel pour la gestion des événements urbains dans une plateforme de ville intelligente.

## 📋 Table des matières

- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [API GraphQL](#api-graphql)
- [Tests](#tests)
- [Docker](#docker)
- [Extension vers base de données](#extension-vers-base-de-données)

## 🏗️ Architecture

```
urban-events-graphql-service/
├── main.py                    # Point d'entrée FastAPI + GraphQL
├── models/                    # Modèles de données
│   ├── __init__.py
│   └── event_models.py        # Event, Zone, EventType, Enums
├── repositories/              # Couche d'accès aux données
│   ├── __init__.py
│   └── data_repository.py     # Repository avec mock data
├── services/                  # Logique métier
│   ├── __init__.py
│   └── event_service.py       # Service des événements
├── graphql_schemas/           # Schémas GraphQL
│   ├── __init__.py
│   ├── types.py               # Types GraphQL
│   ├── queries.py             # Queries GraphQL
│   └── mutations.py           # Mutations GraphQL
├── utils/                     # Utilitaires
│   ├── __init__.py
│   ├── logger.py              # Configuration logging
│   └── middleware.py          # Middleware GraphQL logging
├── tests/                     # Tests unitaires
│   ├── test_repository.py
│   └── test_service.py
├── logs/                      # Répertoire des logs
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Image Docker
└── README.md                  # Documentation
```

## 📦 Installation

### Prérequis

- Python 3.11+
- pip

### Installation locale

```bash
# Cloner le projet
cd urban-events-graphql-service

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le service
python main.py
```

Le service sera accessible sur `http://localhost:8004`

## 🚀 Utilisation

### Endpoints

- **GraphQL**: `http://localhost:8004/graphql`
- **GraphiQL** (interface web): `http://localhost:8004/graphql` (navigateur)
- **Health check**: `http://localhost:8004/health`

### Interface GraphiQL

Ouvrez `http://localhost:8004/graphql` dans votre navigateur pour accéder à l'interface interactive GraphiQL avec:

- Auto-complétion
- Documentation intégrée
- Validation en temps réel

## 📘 API GraphQL

### Types principaux

#### Zone

```graphql
type Zone {
  id: String!
  name: String!
  description: String!
}
```

#### EventType

```graphql
type EventType {
  id: String!
  name: String!
  description: String!
}
```

#### Event

```graphql
type Event {
  id: String!
  name: String!
  description: String!
  eventTypeId: String!
  zoneId: String!
  date: String!
  priority: String! # LOW, MEDIUM, HIGH, CRITICAL
  status: String! # PENDING, IN_PROGRESS, RESOLVED, CANCELLED
  createdAt: String!
  updatedAt: String

  # Relations
  eventType: EventType
  zone: Zone
}
```

### Queries

#### 1. Liste de toutes les zones

```graphql
query {
  zones {
    id
    name
    description
  }
}
```

#### 2. Détails d'une zone

```graphql
query {
  zone(zoneId: "zone-1") {
    id
    name
    description
  }
}
```

#### 3. Liste de tous les événements

```graphql
query {
  events {
    id
    name
    description
    priority
    status
    date
    zone {
      name
    }
    eventType {
      name
    }
  }
}
```

#### 4. Filtrer les événements

```graphql
query {
  events(zoneId: "zone-1", priority: "CRITICAL", status: "IN_PROGRESS") {
    id
    name
    priority
    status
    zone {
      name
    }
  }
}
```

#### 5. Détails d'un événement

```graphql
query {
  event(eventId: "event-1") {
    id
    name
    description
    date
    priority
    status
    eventType {
      name
      description
    }
    zone {
      name
      description
    }
  }
}
```

### Mutations

#### 1. Créer un événement

```graphql
mutation {
  createEvent(
    name: "Nouvel accident"
    description: "Accident sur l'autoroute A1"
    eventTypeId: "type-1"
    zoneId: "zone-2"
    date: "2025-12-05T14:30:00"
    priority: "HIGH"
    status: "PENDING"
  ) {
    success
    message
    event {
      id
      name
      priority
    }
  }
}
```

#### 2. Mettre à jour un événement

```graphql
mutation {
  updateEvent(eventId: "event-1", status: "RESOLVED", priority: "MEDIUM") {
    success
    message
    event {
      id
      status
      priority
      updatedAt
    }
  }
}
```

#### 3. Supprimer un événement

```graphql
mutation {
  deleteEvent(eventId: "event-2") {
    success
    message
  }
}
```

### Exemples de requêtes complexes

#### Événements critiques en cours

```graphql
query CriticalEvents {
  events(priority: "CRITICAL", status: "IN_PROGRESS") {
    id
    name
    description
    date
    zone {
      name
    }
    eventType {
      name
    }
  }
}
```

#### Créer et récupérer un événement

```graphql
mutation CreateAndFetch {
  createEvent(
    name: "Festival annuel"
    description: "Grand événement culturel"
    eventTypeId: "type-3"
    zoneId: "zone-4"
    date: "2025-07-15T10:00:00"
    priority: "LOW"
  ) {
    success
    event {
      id
      name
      eventType {
        name
      }
      zone {
        name
      }
    }
  }
}
```

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/test_repository.py
pytest tests/test_service.py

# Tests avec sortie détaillée
pytest -v
```

### Tests disponibles

- **test_repository.py**: Tests du repository (CRUD, filtres)
- **test_service.py**: Tests de la logique métier

## 🐳 Docker

### Build de l'image

```bash
docker build -t urban-events-graphql-service .
```

### Lancer le conteneur

```bash
docker run -d \
  --name urban-events-service \
  -p 8000:8000 \
  urban-events-graphql-service
```

### Vérifier le service

```bash
# Health check
curl http://localhost:8000/health

# Logs
docker logs urban-events-service

# Arrêter
docker stop urban-events-service
```

### Docker Compose (optionnel)

Créez un fichier `docker-compose.yml`:

```yaml
version: "3.8"

services:
  graphql-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Lancer avec:

```bash
docker-compose up -d
```

## 🔄 Extension vers base de données

Le service est conçu avec une architecture en couches pour faciliter l'intégration d'une vraie base de données.

### Étapes pour intégrer une DB

#### 1. Installer les dépendances DB

```bash
# PostgreSQL
pip install asyncpg sqlalchemy[asyncio]

# MongoDB
pip install motor
```

#### 2. Créer les modèles SQLAlchemy

Dans `models/db_models.py`:

```python
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EventDB(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    # ... autres colonnes
```

#### 3. Modifier le Repository

Dans `repositories/data_repository.py`, remplacez les dictionnaires par des requêtes DB:

```python
async def get_all_events(self) -> List[Event]:
    async with self.session() as session:
        result = await session.execute(select(EventDB))
        events_db = result.scalars().all()
        return [self._to_model(e) for e in events_db]
```

#### 4. Configuration de la connexion

Ajoutez dans `main.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/urban_events"
engine = create_async_engine(DATABASE_URL)
```

### Points d'attention

- ✅ Toute la logique métier reste dans `EventService`
- ✅ Seul le `DataRepository` change
- ✅ Les schémas GraphQL ne sont pas impactés
- ✅ Les tests doivent être adaptés pour utiliser une DB de test

## 📝 Logging

Le service log automatiquement:

- Toutes les requêtes GraphQL
- Durée d'exécution
- Erreurs éventuelles
- Health checks

Logs disponibles dans la console et le répertoire `logs/` (si configuré).

## 🔒 Bonnes pratiques implémentées

- ✅ Architecture en couches (models, repositories, services, schemas)
- ✅ Séparation des responsabilités
- ✅ Validation des entrées
- ✅ Gestion des erreurs GraphQL
- ✅ Logging structuré
- ✅ Tests unitaires
- ✅ Documentation automatique (SDL GraphQL)
- ✅ Healthcheck
- ✅ Dockerisation
- ✅ Code commenté et maintenable

## 🤝 Intégration avec autres microservices

Ce service GraphQL peut être intégré avec:

- **REST services** (mobilité)
- **SOAP services** (qualité de l'air)
- **gRPC services** (urgences)

Via une **API Gateway** qui orchestre tous les services.

## 📞 Support

Pour toute question ou contribution:

- Documentation GraphQL: `/graphql` (interface GraphiQL)
- Health check: `/health`
- Logs: Consultez les logs du conteneur

## 🎯 Roadmap

- [ ] Authentification JWT
- [ ] Rate limiting
- [ ] Pagination des résultats
- [ ] Subscriptions GraphQL (temps réel)
- [ ] Cache Redis
- [ ] Metrics Prometheus
- [ ] CI/CD pipeline

---

**Version**: 1.0.0  
**Auteur**: Équipe Smart City Platform  
**License**: MIT
