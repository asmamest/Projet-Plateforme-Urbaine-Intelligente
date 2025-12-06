FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copie des requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Génération des fichiers proto
RUN python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./protos \
    --grpc_python_out=./protos \
    ./protos/emergency.proto

# Exposition du port gRPC
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import grpc; from protos import emergency_pb2, emergency_pb2_grpc; \
    channel = grpc.insecure_channel('localhost:50051'); \
    stub = emergency_pb2_grpc.EmergencyAlertServiceStub(channel); \
    stub.HealthCheck(emergency_pb2.HealthCheckRequest(), timeout=5)"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV GRPC_PORT=50051

# Commande de démarrage
CMD ["python", "-m", "src.server"]