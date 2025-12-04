FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Création du dossier logs
RUN mkdir -p logs

# Exposition du port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health', timeout=2)"

# Démarrage du service
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8001", "--timeout", "120", "main:app"]