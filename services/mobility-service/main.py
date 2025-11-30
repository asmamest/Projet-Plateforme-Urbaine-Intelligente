"""
Point d'entrée principal de l'application FastAPI
Service de Mobilité Intelligente pour plateforme urbaine
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import yaml

# Import des routes
from routes import horaires, trafic, disponibilite, lignes

# Import du middleware
from middleware.logging_middleware import LoggingMiddleware

# Import de la configuration
from config.settings import settings

# Configuration du logging
logger = logging.getLogger("mobility-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    logger.info("🚀 Démarrage du Service de Mobilité Intelligente")
    logger.info(f"📍 Version: {settings.app_version}")
    logger.info(f"🌐 Mode debug: {settings.debug}")
    
    # Export de la documentation OpenAPI au démarrage
    try:
        with open("openapi.yaml", "w") as f:
            yaml.dump(app.openapi(), f, allow_unicode=True, default_flow_style=False)
        logger.info("✅ Documentation OpenAPI générée: openapi.yaml")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération OpenAPI: {e}")
    
    yield
    
    logger.info("🛑 Arrêt du Service de Mobilité Intelligente")

# Création de l'application FastAPI
app = FastAPI(
    title=settings.app_name,
    description="""
    ## Service REST de Mobilité Intelligente
    
    Ce service fait partie de la plateforme urbaine intelligente et fournit:
    
    * 📅 **Consultation des horaires** de transport en temps réel
    * 🚦 **État du trafic** avec retards et perturbations
    * 🚌 **Disponibilité des véhicules** par ligne
    * 🔧 **Gestion CRUD complète** des lignes de transport
    
    ### Architecture
    
    - **Protocole**: REST API (FastAPI)
    - **Format**: JSON
    - **Documentation**: OpenAPI 3.0
    - **Conteneurisation**: Docker
    
    ### Endpoints principaux
    
    - `GET /horaires/{ligne}` - Horaires d'une ligne
    - `GET /trafic` - État du trafic global
    - `GET /disponibilite` - Disponibilité des véhicules
    - `GET /lignes` - Liste des lignes
    - `POST /lignes` - Créer une ligne
    - `PUT /lignes/{id}` - Modifier une ligne
    - `DELETE /lignes/{id}` - Supprimer une ligne
    """,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ajout du middleware de logging
app.add_middleware(LoggingMiddleware)

# Enregistrement des routes
app.include_router(horaires.router)
app.include_router(trafic.router)
app.include_router(disponibilite.router)
app.include_router(lignes.router)

# ============================================================================
# ROUTES SYSTÈME
# ============================================================================

@app.get("/", tags=["Système"], summary="Page d'accueil")
async def root():
    """
    Point d'entrée principal de l'API.
    Retourne les informations de base du service.
    """
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "documentation": "/docs",
        "endpoints": {
            "horaires": "/horaires/{ligne}",
            "trafic": "/trafic",
            "disponibilite": "/disponibilite",
            "lignes": "/lignes"
        }
    }

@app.get("/health", tags=["Système"], summary="Health check")
async def health_check():
    """
    Endpoint de vérification de santé du service.
    Utilisé par Docker et les orchestrateurs (Kubernetes, etc.)
    
    Retourne:
    - **status**: État du service (healthy/unhealthy)
    - **version**: Version de l'application
    - **uptime**: Temps depuis le démarrage
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }

# ============================================================================
# GESTIONNAIRE D'ERREURS GLOBAL
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Gestionnaire d'erreurs global pour capturer toutes les exceptions non gérées
    """
    logger.error(f"Erreur non gérée: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Erreur interne du serveur",
            "message": str(exc) if settings.debug else "Une erreur s'est produite",
            "path": str(request.url)
        }
    )

# ============================================================================
# POINT D'ENTRÉE POUR EXÉCUTION DIRECTE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
    
    