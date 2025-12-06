"""
Serveur gRPC principal
"""
import grpc
from concurrent import futures
import signal
import sys
import os

from src.services.emergency_service import EmergencyAlertService
from src.utils.logger import setup_logger
from protos import emergency_pb2_grpc

# Logger
server_logger = setup_logger('grpc_server')


def serve():
    """Démarre le serveur gRPC"""
    # Configuration du serveur
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
            ('grpc.so_reuseport', 1),
            ('grpc.use_local_subchannel_pool', 1),
        ],
        compression=grpc.Compression.Gzip
    )
    
    # Enregistrement du service
    emergency_pb2_grpc.add_EmergencyAlertServiceServicer_to_server(
        EmergencyAlertService(), server
    )
    
    # Port d'écoute
    port = os.getenv('GRPC_PORT', '50051')
    server.add_insecure_port(f'[::]:{port}')
    
    # Démarrage
    server.start()
    server_logger.info(f"=" * 70)
    server_logger.info(f"🚀 Emergency Alert gRPC Service started")
    server_logger.info(f"=" * 70)
    server_logger.info(f"📍 gRPC Server: localhost:{port}")
    server_logger.info(f"💚 Health Check: Invoke HealthCheck RPC")
    server_logger.info(f"📊 Metrics: Ready for Prometheus")
    server_logger.info(f"=" * 70)
    
    # Graceful shutdown
    def signal_handler(sig, frame):
        server_logger.info("Shutting down gracefully...")
        server.stop(grace=5)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Attente
    server.wait_for_termination()


if __name__ == '__main__':
    serve()