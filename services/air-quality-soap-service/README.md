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
