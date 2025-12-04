# Air Quality SOAP Service

Service SOAP pour la gestion de la qualité de l'air dans une plateforme Smart City.

## 📋 Fonctionnalités

### Méthodes SOAP disponibles

1. **GetAQI(zone)** - Obtenir l'indice de qualité de l'air
2. **GetPollutants(zone)** - Obtenir les niveaux de polluants
3. **CompareZones(zoneA, zoneB)** - Comparer deux zones
4. **GetHistory(zone, startDate, endDate, granularity)** - Obtenir l'historique
5. **FilterPollutants(zone, threshold)** - Filtrer les polluants par seuil
6. **HealthCheck()** - Vérifier l'état du service

## 🚀 Installation

### Prérequis

- Python 3.10+
- Docker & Docker Compose (optionnel)

### Installation locale

```bash
# Cloner le projet
git clone <repository>
cd air-quality-soap-service

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Créer fichier .env
cp .env.example .env

# Lancer le serveur
python main.py
```

Le service sera disponible sur `http://localhost:8000`

### Installation Docker

```bash
# Build et lancement
docker-compose up --build

# En arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

## 📖 Utilisation

### Accéder au WSDL

http://localhost:8000/?wsdl

### Tester avec le client Python

```bash
# Assurer que le service est lancé
python test_soap_client.py
```

### Exemples de requêtes SOAP

Voir le fichier `docs/soap_examples.xml` pour tous les exemples.

#### Exemple: GetAQI

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:tns="http://smartcity.air-quality.soap">
   <soapenv:Body>
      <tns:GetAQI>
         <tns:zone>downtown</tns:zone>
      </tns:GetAQI>
   </soapenv:Body>
</soapenv:Envelope>
```

#### Exemple: CompareZones

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:tns="http://smartcity.air-quality.soap">
   <soapenv:Body>
      <tns:CompareZones>
         <tns:zoneA>park</tns:zoneA>
         <tns:zoneB>industrial</tns:zoneB>
      </tns:CompareZones>
   </soapenv:Body>
</soapenv:Envelope>
```

### Zones disponibles (mock data)

- `downtown` - Centre-ville
- `industrial` - Zone industrielle
- `residential` - Zone résidentielle
- `park` - Parc urbain
- `suburb` - Banlieue
- `airport` - Aéroport
- `harbor` - Port
- `university` - Campus universitaire

## 🧪 Tests

### Lancer les tests unitaires

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=. --cov-report=html

# Tests spécifiques
pytest tests/test_service.py
pytest tests/test_repository.py
```

### Linter

```bash
# Avec ruff
ruff check .

# Auto-fix
ruff check --fix .
```

## 📊 Structure du projet

```
air-quality-soap-service/
├── main.py # Point d'entrée du service SOAP
├── models/ # Définitions des modèles de données
│ ├── **init**.py
│ └── air_quality_models.py # Modèles pour la qualité de l'air (AQI, polluants, etc.)
├── services/ # Logique métier du service SOAP
│ ├── **init**.py
│ └── air_quality_service.py# Implémentation de AirQualityService
├── repositories/ # Accès aux données
│ ├── **init**.py
│ └── data_repository.py # Gestion des sources de données (CSV, DB, etc.)
├── utils/ # Fonctions utilitaires
│ ├── **init**.py
│ └── logger.py # Configuration et gestion des logs
├── wsdl/ # Définition du service SOAP
│ └── air_quality.wsdl # WSDL décrivant le service
├── docs/ # Documentation et exemples
│ └── soap_examples.xml # Exemples de requêtes/réponses SOAP
├── logs/ # Stockage des logs générés
│ └── .gitkeep
├── tests/ # Tests unitaires et d’intégration
│ ├── **init**.py
│ ├── test_service.py # Tests du service AirQualityService
│ └── test_repository.py # Tests du repository de données
├── data/ # Données statiques ou d’exemple
│ └── air_quality_data.csv # Jeu de données pour tests ou simulation
├── test_soap_client.py # Script de test client SOAP
├── Dockerfile # Configuration pour containerisation
├── docker-compose.yml # Déploiement multi-services
├── requirements.txt # Dépendances Python
├── .env.example # Exemple de fichier de configuration environnement
└── README.md # Documentation du projet
```
