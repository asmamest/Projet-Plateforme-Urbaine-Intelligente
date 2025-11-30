"""
Routes pour l'état du trafic
"""
from fastapi import APIRouter
from services.trafic_service import TraficService
from schemas.trafic import TraficResponse, TraficItem
from datetime import datetime

router = APIRouter(prefix="/trafic", tags=["Trafic"])
service = TraficService()

@router.get("", response_model=TraficResponse, summary="Obtenir l'état du trafic")
async def get_trafic():
    """
    Récupère l'état du trafic en temps réel pour toutes les lignes.
    
    Retourne pour chaque ligne:
    - Le statut actuel (normal, retard, annulé, perturbé)
    - Le retard estimé en minutes
    - Un message d'information si nécessaire
    """
    etats_trafic = service.get_all_trafic()
    
    return TraficResponse(
        derniere_maj=datetime.now(),
        nombre_lignes=len(etats_trafic),
        trafic=[
            TraficItem(
                ligne_id=e.ligne_id,
                statut=e.statut.value,
                retard_minutes=e.retard_minutes,
                message=e.message,
                timestamp=e.timestamp
            ) for e in etats_trafic
        ]
    )