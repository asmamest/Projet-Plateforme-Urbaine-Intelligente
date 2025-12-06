#!/bin/bash
# Script pour générer les fichiers Python depuis les protos
# et corriger les imports relatifs pour gRPC

PROTO_DIR="./protos"

echo "🔨 Génération des fichiers Protocol Buffers..."

python -m grpc_tools.protoc \
    -I="$PROTO_DIR" \
    --python_out="$PROTO_DIR" \
    --grpc_python_out="$PROTO_DIR" \
    "$PROTO_DIR/emergency.proto"

# Ajouter un __init__.py dans le dossier protos si absent
if [ ! -f "$PROTO_DIR/__init__.py" ]; then
    touch "$PROTO_DIR/__init__.py"
fi

# Corriger l'import dans emergency_pb2_grpc.py pour utiliser import relatif
sed -i "s/^import emergency_pb2/from . import emergency_pb2/" "$PROTO_DIR/emergency_pb2_grpc.py"

echo "✅ Fichiers générés avec succès dans $PROTO_DIR"
echo "   - emergency_pb2.py"
echo "   - emergency_pb2_grpc.py"
