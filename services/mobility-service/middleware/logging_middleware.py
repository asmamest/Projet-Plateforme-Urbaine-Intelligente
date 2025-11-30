"""
Middleware de logging pour tracer toutes les requêtes HTTP
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mobility-service")

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware pour logger toutes les requêtes entrantes et sortantes"""
    
    async def dispatch(self, request: Request, call_next):
        # Capture du temps de début
        start_time = time.time()
        
        # Log de la requête entrante
        logger.info(
            f"Requête entrante: {request.method} {request.url.path} "
            f"- Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Traitement de la requête
        response = await call_next(request)
        
        # Calcul du temps de traitement
        process_time = time.time() - start_time
        
        # Log de la réponse
        logger.info(
            f"Requête traitée: {request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Durée: {process_time:.3f}s"
        )
        
        # Ajout d'un header custom avec le temps de traitement
        response.headers["X-Process-Time"] = str(process_time)
        
        return response