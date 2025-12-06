# 🚌 Service REST - Mobilité Intelligente

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Microservice REST professionnel pour la gestion des transports urbains intelligents dans le cadre de la plateforme de services urbains interopérables.

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Caractéristiques](#-caractéristiques)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Base de données](#-base-de-données)
- [Tests](#-tests)
- [Déploiement](#-déploiement)
- [Monitoring](#-monitoring)
- [Contribution](#-contribution)
- [License](#-license)

---

## 🎯 Vue d'ensemble

Le **Service Mobilité Intelligente** est un microservice REST construit avec FastAPI qui fournit des informations en temps réel sur les transports publics urbains :

- 🚍 **Horaires** : Consultation des horaires de bus, métro et tramway
- 🚦 **État du trafic** : Retards, perturbations et incidents en temps réel
- 🚌 **Disponibilité** : Nombre de véhicules en service par ligne
- 🔧 **Gestion CRUD** : Administration complète des lignes de transport

### Cas d'usage

- **Citoyens** : Planifier leurs trajets avec des informations actualisées
- **Opérateurs** : Gérer et monitorer les lignes de transport
- **Développeurs** : Intégrer des données de mobilité dans leurs applications
- **Administrations** : Analyser et optimiser les services de transport

---

## ✨ Caractéristiques

### Fonctionnalités métier

- ✅ **Consultation des horaires** par ligne avec détails (quai, destination)
- ✅ **État du trafic** en temps réel (retards, annulations, perturbations)
- ✅ **Disponibilité des véhicules** avec taux de service
- ✅ **CRUD complet** pour la gestion des lignes de transport
- ✅ **Validation** stricte des entrées avec messages d'erreur explicites

### Caractéristiques techniques

- 🏗️ **Architecture en couches** : Routes → Services → Repositories
- 🗄️ **Base de données PostgreSQL** avec SQLAlchemy ORM
- 📝 **Documentation OpenAPI** automatique et interactive
- 🔐 **Validation Pydantic** pour toutes les entrées
- 📊 **Logging middleware** avec traçabilité des requêtes
- 🏥 **Health checks** pour orchestration K8s
- 🐳 **Dockerisé** avec docker-compose
- ✅ **Tests unitaires** avec pytest
- 🔄 **Prêt pour CI/CD**

---

## 🏗️ Architecture

### Structure du projet

```
mobility-service/
├── main.py                          # Point d'entrée FastAPI
├── requirements.txt                 # Dépendances Python
├── Dockerfile                       # Image Docker
├── docker-compose.yml               # Orchestration services
├── .env                            # Variables d'environnement
├── README.md                        # Documentation
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration centralisée
├── database/
│   ├── __init__.py
│   ├── connection.py               # Connexion PostgreSQL
│   └── models.py                   # Modèles SQLAlchemy
├── models/
│   ├── __init__.py
│   └── entities.py                 # Entités métier (domain)
├── schemas/
│   ├── __init__.py
│   ├── ligne.py                    # Schémas Pydantic lignes
│   ├── horaire.py                  # Schémas Pydantic horaires
│   ├── trafic.py                   # Schémas Pydantic trafic
│   └── disponibilite.py            # Schémas Pydantic disponibilité
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py          # Interface repository abstraite
│   ├── ligne_repository.py         # Accès données lignes
│   ├── horaire_repository.py       # Accès données horaires
│   ├── trafic_repository.py        # Accès données trafic
│   └── disponibilite_repository.py # Accès données disponibilité
├── services/
│   ├── __init__.py
│   ├── ligne_service.py            # Logique métier lignes
│   ├── horaire_service.py          # Logique métier horaires
│   ├── trafic_service.py           # Logique métier trafic
│   └── disponibilite_service.py    # Logique métier disponibilité
├── routes/
│   ├── __init__.py
│   ├── lignes.py                   # Endpoints CRUD lignes
│   ├── horaires.py                 # Endpoints horaires
│   ├── trafic.py                   # Endpoints trafic
│   └── disponibilite.py            # Endpoints disponibilité
├── middleware/
│   ├── __init__.py
│   └── logging_middleware.py       # Middleware logging HTTP
└── tests/
    ├── __init__.py
    ├── test_services.py
    └── test_repositories.py
```

### Flux de données

```
┌─────────────┐
│   Client    │
│ (HTTP/REST) │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│          FastAPI Application            │
│  ┌────────────────────────────────────┐ │
│  │     Middleware (Logging, CORS)     │ │
│  └────────────┬───────────────────────┘ │
│               ▼                          │
│  ┌────────────────────────────────────┐ │
│  │          Routes Layer              │ │
│  │   (horaires, trafic, lignes...)    │ │
│  └────────────┬───────────────────────┘ │
│               ▼                          │
│  ┌────────────────────────────────────┐ │
│  │        Services Layer              │ │
│  │   (Logique métier, validation)     │ │
│  └────────────┬───────────────────────┘ │
│               ▼                          │
│  ┌────────────────────────────────────┐ │
│  │       Repositories Layer           │ │
│  │   (Abstraction accès données)      │ │
│  └────────────┬───────────────────────┘ │
└───────────────┼─────────────────────────┘
                ▼
       ┌─────────────────┐
       │   PostgreSQL    │
       │   (smart_city)  │
       └─────────────────┘
```

### Modèle de données

```sql
-- Table: lignes
CREATE TABLE lignes (
    id VARCHAR(36) PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    type_transport VARCHAR(20) NOT NULL,  -- bus, metro, train, tramway
    terminus_debut VARCHAR(255) NOT NULL,
    terminus_fin VARCHAR(255) NOT NULL,
    actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table: horaires
CREATE TABLE horaires (
    id VARCHAR(36) PRIMARY KEY,
    ligne_id VARCHAR(36) REFERENCES lignes(id) ON DELETE CASCADE,
    destination VARCHAR(255) NOT NULL,
    heure_depart VARCHAR(5) NOT NULL,
    heure_arrivee VARCHAR(5) NOT NULL,
    station VARCHAR(255) NOT NULL,
    quai VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: etats_trafic
CREATE TABLE etats_trafic (
    id VARCHAR(36) PRIMARY KEY,
    ligne_id VARCHAR(36) REFERENCES lignes(id) ON DELETE CASCADE,
    statut VARCHAR(20) NOT NULL,  -- normal, retard, annule, perturbe
    retard_minutes INTEGER DEFAULT 0,
    message TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: disponibilites
CREATE TABLE disponibilites (
    id VARCHAR(36) PRIMARY KEY,
    ligne_id VARCHAR(36) REFERENCES lignes(id) ON DELETE CASCADE,
    vehicules_total INTEGER NOT NULL,
    vehicules_en_service INTEGER NOT NULL,
    taux_disponibilite FLOAT NOT NULL,
    derniere_maj TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 Installation

### Prérequis

- **Python** 3.11 ou supérieur
- **PostgreSQL** 15 ou supérieur
- **Docker** et **Docker Compose** (optionnel mais recommandé)
- **Git**

### Installation locale

#### 1. Cloner le projet

```bash
git clone https://github.com/votre-org/smart-city-platform.git
cd smart-city-platform/services/mobility-service
```

#### 2. Créer un environnement virtuel

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configuration

Créer un fichier `.env` à la racine :

```bash
cp .env.example .env
```

Éditer `.env` avec vos paramètres :

```env
# Application
APP_NAME=Service Mobilite Intelligente
APP_VERSION=1.0.0
DEBUG=True

# Base de données
DATABASE_URL=postgresql://smart_city_user:smart_city_pass@localhost:5432/smart_city_db
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Serveur
HOST=0.0.0.0
PORT=8000
```

#### 5. Démarrer PostgreSQL

```bash
# Avec Docker Compose
docker-compose up -d postgres

# Attendre que PostgreSQL soit prêt
docker logs -f smart-city-postgres
```

#### 6. Lancer le service

```bash
python main.py
```

Le service sera accessible sur **http://localhost:8000**

---

## ⚙️ Configuration

### Variables d'environnement

| Variable                | Description                  | Défaut                        | Obligatoire |
| ----------------------- | ---------------------------- | ----------------------------- | ----------- |
| `APP_NAME`              | Nom de l'application         | Service Mobilite Intelligente | Non         |
| `APP_VERSION`           | Version                      | 1.0.0                         | Non         |
| `DEBUG`                 | Mode debug                   | True                          | Non         |
| `HOST`                  | Adresse d'écoute             | 0.0.0.0                       | Non         |
| `PORT`                  | Port d'écoute                | 8000                          | Non         |
| `DATABASE_URL`          | URL PostgreSQL               | -                             | **Oui**     |
| `DATABASE_POOL_SIZE`    | Taille du pool de connexions | 5                             | Non         |
| `DATABASE_MAX_OVERFLOW` | Connexions supplémentaires   | 10                            | Non         |

### Fichier de configuration

`config/settings.py` :

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Service Mobilite Intelligente"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str
    database_pool_size: int = 5
    database_max_overflow: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## 📖 Utilisation

### Démarrage rapide

```bash
# 1. Démarrer tous les services avec Docker Compose
docker-compose up -d

# 2. Vérifier l'état du service
curl http://localhost:8000/health

# 3. Accéder à la documentation interactive
open http://localhost:8000/docs
```

### Exemples de requêtes

#### 1. Consulter les horaires d'une ligne

```bash
curl http://localhost:8000/horaires/L1
```

**Réponse :**

```json
{
  "ligne": "L1",
  "nombre_horaires": 3,
  "horaires": [
    {
      "id": "h1",
      "ligne_id": "1",
      "destination": "Banlieue Nord",
      "heure_depart": "08:00",
      "heure_arrivee": "08:25",
      "station": "Gare Centrale",
      "quai": "A"
    },
    {
      "id": "h2",
      "ligne_id": "1",
      "destination": "Banlieue Nord",
      "heure_depart": "08:15",
      "heure_arrivee": "08:40",
      "station": "Gare Centrale",
      "quai": "A"
    }
  ]
}
```

#### 2. Obtenir l'état du trafic

```bash
curl http://localhost:8000/trafic
```

**Réponse :**

```json
{
  "derniere_maj": "2025-12-06T10:30:00",
  "nombre_lignes": 4,
  "trafic": [
    {
      "ligne_id": "1",
      "statut": "normal",
      "retard_minutes": 0,
      "message": "Trafic fluide",
      "timestamp": "2025-12-06T10:30:00"
    },
    {
      "ligne_id": "2",
      "statut": "retard",
      "retard_minutes": 5,
      "message": "Retard dû à un incident technique",
      "timestamp": "2025-12-06T10:28:00"
    }
  ]
}
```

#### 3. Vérifier la disponibilité des véhicules

```bash
curl http://localhost:8000/disponibilite
```

**Réponse :**

```json
{
  "timestamp": "2025-12-06T10:35:00",
  "nombre_lignes": 4,
  "disponibilites": [
    {
      "ligne_id": "1",
      "vehicules_total": 20,
      "vehicules_en_service": 18,
      "taux_disponibilite": 90.0,
      "derniere_maj": "2025-12-06T10:30:00"
    }
  ]
}
```

#### 4. Créer une nouvelle ligne

```bash
curl -X POST http://localhost:8000/lignes \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "L3",
    "nom": "Ligne 3 - Périphérique",
    "type_transport": "metro",
    "terminus_debut": "Station Nord",
    "terminus_fin": "Station Sud",
    "actif": true
  }'
```

**Réponse :**

```json
{
  "id": "a3f2e1b9-c4d8-4e5f-9a1b-2c3d4e5f6a7b",
  "numero": "L3",
  "nom": "Ligne 3 - Périphérique",
  "type_transport": "metro",
  "terminus_debut": "Station Nord",
  "terminus_fin": "Station Sud",
  "actif": true,
  "created_at": "2025-12-06T10:40:00",
  "updated_at": "2025-12-06T10:40:00"
}
```

#### 5. Mettre à jour une ligne

```bash
curl -X PUT http://localhost:8000/lignes/a3f2e1b9-c4d8-4e5f-9a1b-2c3d4e5f6a7b \
  -H "Content-Type: application/json" \
  -d '{
    "actif": false
  }'
```

#### 6. Supprimer une ligne

```bash
curl -X DELETE http://localhost:8000/lignes/a3f2e1b9-c4d8-4e5f-9a1b-2c3d4e5f6a7b
```

---

## 📚 API Documentation

### Documentation interactive

Une fois le service lancé, accédez à la documentation interactive :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **OpenAPI JSON** : http://localhost:8000/openapi.json
- **OpenAPI YAML** : `openapi.yaml` (généré au démarrage)

### Endpoints disponibles

#### Système

| Méthode | Endpoint  | Description                                 |
| ------- | --------- | ------------------------------------------- |
| GET     | `/`       | Page d'accueil avec informations du service |
| GET     | `/health` | Health check pour orchestration             |

#### Horaires

| Méthode | Endpoint            | Description                        |
| ------- | ------------------- | ---------------------------------- |
| GET     | `/horaires/{ligne}` | Consulter les horaires d'une ligne |

**Paramètres :**

- `ligne` (path) : Numéro de la ligne (ex: L1, B15)

**Réponse :** `HorairesResponse`

#### Trafic

| Méthode | Endpoint  | Description                                   |
| ------- | --------- | --------------------------------------------- |
| GET     | `/trafic` | Obtenir l'état du trafic de toutes les lignes |

**Réponse :** `TraficResponse`

#### Disponibilité

| Méthode | Endpoint         | Description                            |
| ------- | ---------------- | -------------------------------------- |
| GET     | `/disponibilite` | Obtenir la disponibilité des véhicules |

**Réponse :** `DisponibiliteResponse`

#### Lignes (CRUD)

| Méthode | Endpoint       | Description              |
| ------- | -------------- | ------------------------ |
| GET     | `/lignes`      | Lister toutes les lignes |
| POST    | `/lignes`      | Créer une nouvelle ligne |
| PUT     | `/lignes/{id}` | Mettre à jour une ligne  |
| DELETE  | `/lignes/{id}` | Supprimer une ligne      |

**Schémas :**

```python
# LigneCreate
{
  "numero": "L1",
  "nom": "Ligne 1 - Centre Nord",
  "type_transport": "metro",  # bus, metro, train, tramway
  "terminus_debut": "Gare Centrale",
  "terminus_fin": "Banlieue Nord",
  "actif": true
}

# LigneUpdate (tous les champs optionnels)
{
  "numero": "L1",
  "nom": "Ligne 1 - Nouvelle destination",
  "actif": false
}

# LigneResponse
{
  "id": "uuid",
  "numero": "L1",
  "nom": "Ligne 1 - Centre Nord",
  "type_transport": "metro",
  "terminus_debut": "Gare Centrale",
  "terminus_fin": "Banlieue Nord",
  "actif": true,
  "created_at": "2025-12-06T10:00:00",
  "updated_at": "2025-12-06T10:00:00"
}
```

### Codes de statut HTTP

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | Succès                               |
| 201  | Ressource créée                      |
| 204  | Suppression réussie (pas de contenu) |
| 400  | Requête invalide                     |
| 404  | Ressource introuvable                |
| 500  | Erreur serveur interne               |

---

## 🗄️ Base de données

### Connexion PostgreSQL

Le service utilise SQLAlchemy pour l'ORM avec PostgreSQL.

**Fichier :** `database/connection.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:pass@localhost:5432/db"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"client_encoding": "utf8"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Initialisation

Au démarrage, le service :

1. **Crée les tables** si elles n'existent pas
2. **Insère des données initiales** (seed data) si la base est vide

```python
# Dans main.py
from database.connection import init_db, seed_data

init_db()      # Crée les tables
seed_data()    # Insère les données mockées
```

### Migration (futur)

Pour les migrations de schéma, utiliser **Alembic** :

```bash
# Initialiser Alembic
alembic init alembic

# Créer une migration
alembic revision --autogenerate -m "Add new column"

# Appliquer les migrations
alembic upgrade head
```

---

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/test_services.py -v

# Tests avec logs
pytest -s
```

### Structure des tests

```
tests/
├── __init__.py
├── conftest.py                 # Fixtures pytest
├── test_repositories.py        # Tests repositories
├── test_services.py            # Tests services
└── test_routes.py              # Tests endpoints API
```

### Exemple de test

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_horaires():
    """Test GET /horaires/L1"""
    response = client.get("/horaires/L1")
    assert response.status_code == 200
    data = response.json()
    assert data["ligne"] == "L1"
    assert "horaires" in data

def test_create_ligne():
    """Test POST /lignes"""
    ligne_data = {
        "numero": "TEST1",
        "nom": "Ligne Test",
        "type_transport": "bus",
        "terminus_debut": "A",
        "terminus_fin": "B",
        "actif": True
    }
    response = client.post("/lignes", json=ligne_data)
    assert response.status_code == 201
    assert response.json()["numero"] == "TEST1"
```

---

## 🐳 Déploiement

### Docker Compose (Développement)

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker logs -f mobility-service

# Arrêter
docker-compose down
```

**Fichier :** `docker-compose.yml`

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15-alpine
    container_name: smart-city-postgres
    environment:
      POSTGRES_USER: smart_city_user
      POSTGRES_PASSWORD: smart_city_pass
      POSTGRES_DB: smart_city_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U smart_city_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  mobility-service:
    build: .
    container_name: mobility-service
    environment:
      DATABASE_URL: postgresql://smart_city_user:smart_city_pass@postgres:5432/smart_city_db
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - .:/app

volumes:
  postgres_data:
```

### Kubernetes (Production)

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mobility-service
  labels:
    app: mobility-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mobility-service
  template:
    metadata:
      labels:
        app: mobility-service
    spec:
      containers:
        - name: mobility-service
          image: registry.example.com/mobility-service:1.0.0
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mobility-service
spec:
  type: ClusterIP
  selector:
    app: mobility-service
  ports:
    - port: 80
      targetPort: 8000
```

#### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mobility-service-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - api.smart-city.example.com
      secretName: mobility-tls
  rules:
    - host: api.smart-city.example.com
      http:
        paths:
          - path: /mobility
            pathType: Prefix
            backend:
              service:
                name: mobility-service
                port:
                  number: 80
```

---

## 📊 Monitoring

### Logs

Les logs sont structurés et incluent :

- Timestamp
- Niveau (INFO, WARNING, ERROR)
- Méthode HTTP
- Endpoint
- Durée de traitement
- IP client

**Exemple de log :**

```
2025-12-06 10:30:45,123 - mobility-service - INFO - Requête entrante: GET /horaires/L1 - Client: 192.168.1.10
2025-12-06 10:30:45,156 - mobility-service - INFO - Requête traitée: GET /horaires/L1 - Status: 200 - Durée: 0.033s
```

### Métriques (futur)

Pour Prometheus :

```python
from prometheus_client import Counter, Histogram

requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)
```

### Health checks

```bash
# Vérifier l'état du service
curl http://localhost:8000/health

# Réponse
{
  "status": "healthy",
  "service": "Service Mobilite Intelligente",
  "version": "1.0.0"
}
```

---

## 🤝 Contribution

### Guide de contribution

1. **Fork** le projet
2. Créer une **branche** : `git checkout -b feature/nouvelle-fonctionnalite`
3. **Commit** vos changements : `git commit -m 'Ajout nouvelle fonctionnalité'`
4. **Push** vers la branche : `git push origin feature/nouvelle-fonctionnalite`
5. Ouvrir une **Pull Request**

### Standards de code

- **PEP 8** : Style guide Python
- **Type hints** : Typage statique
- **Docstrings** : Documentation des fonctions
- **Tests** : Couverture minimum 80%

### Linter

```bash
# Installer ruff
pip install ruff

# Vérifier le code
ruff check .

# Formatter
ruff format .
```

---

## 📄 License

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Auteurs

- **Équipe Projet SOC** - Plateforme Intelligente de Services Urbains
- Université de Tunis - Master SOA/SOC

---

## 📞 Support

Pour toute question ou problème :

- **Issues GitHub** : https://github.com/votre-org/smart-city-platform/issues
- **Email** : support@smart-city.example.com
- **Documentation** : https://docs.smart-city.example.com

---

## 🔗 Liens utiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

---

**🎯 Service prêt pour l'intégration avec API Gateway et autres microservices !**
