"""
Routes pour la disponibilité des véhicules
"""
from fastapi import APIRouter
from services.disponibilite_service import DisponibiliteService
from schemas.disponibilite import DisponibiliteResponse, DisponibiliteItem
from datetime import datetime

router = APIRouter(prefix="/disponibilite", tags=["Disponibilité"])
service = DisponibiliteService()

@router.get("", response_model=DisponibiliteResponse, summary="Obtenir la disponibilité des véhicules")
async def get_disponibilite():
    """
    Récupère la disponibilité des véhicules pour toutes les lignes.
    
    Retourne pour chaque ligne:
    - Le nombre total de véhicules
    - Le nombre de véhicules actuellement en service
    - Le taux de disponibilité en pourcentage
    """
    disponibilites = service.get_all_disponibilites()
    
    return DisponibiliteResponse(
        timestamp=datetime.now(),
        nombre_lignes=len(disponibilites),
        disponibilites=[
            DisponibiliteItem(
                ligne_id=d.ligne_id,
                vehicules_total=d.vehicules_total,
                vehicules_en_service=d.vehicules_en_service,
                taux_disponibilite=d.taux_disponibilite,
                derniere_maj=d.derniere_maj
            ) for d in disponibilites
        ]
    )
