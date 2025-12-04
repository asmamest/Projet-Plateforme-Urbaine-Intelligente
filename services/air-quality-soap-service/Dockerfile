FROM python:3.10-slim

LABEL maintainer="air-quality-service"
LABEL description="Air Quality SOAP Service pour plateforme Smart City"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    LOG_LEVEL=INFO \
    WORKERS=4

# Créer répertoire de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer dossiers nécessaires
RUN mkdir -p logs data wsdl

# Exposer le port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/?wsdl')"

# Commande de démarrage avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "main:create_app()"]