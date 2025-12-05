"""
Middleware pour logging des requêtes GraphQL
"""
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("urban-events-service")


class GraphQLLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware pour logger les requêtes GraphQL"""
    
    async def dispatch(self, request: Request, call_next):
        # Début du timer
        start_time = time.time()
        
        # Extraction du type de requête si c'est GraphQL
        if request.url.path == "/graphql":
            try:
                body = await request.body()
                request_info = body.decode('utf-8')[:200]  # Premiers 200 chars
                logger.info(f"GraphQL Request: {request_info}")
            except:
                pass
        
        # Traitement de la requête
        response = await call_next(request)
        
        # Calcul de la durée
        duration = time.time() - start_time
        
        # Log de la réponse
        logger.info(
            f"Path: {request.url.path} | "
            f"Method: {request.method} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.3f}s"
        )
        
        return response