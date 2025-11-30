"""
Routes pour la consultation des horaires
"""
from fastapi import APIRouter, HTTPException, Path
from services.horaire_service import HoraireService
from schemas.horaire import HorairesResponse, HoraireItem

router = APIRouter(prefix="/horaires", tags=["Horaires"])
service = HoraireService()

@router.get("/{ligne}", response_model=HorairesResponse, summary="Consulter les horaires d'une ligne")
async def get_horaires(
    ligne: str = Path(..., description="Numéro de la ligne (ex: L1, B15)", example="L1")
):
    """
    Récupère tous les horaires de passage pour une ligne donnée.
    
    - **ligne**: Numéro de la ligne à consulter
    
    Retourne la liste complète des horaires avec les informations de départ, arrivée et quai.
    """
    horaires = service.get_horaires_by_ligne(ligne)
    
    if not horaires:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun horaire trouvé pour la ligne {ligne}"
        )
    
    return HorairesResponse(
        ligne=ligne,
        nombre_horaires=len(horaires),
        horaires=[
            HoraireItem(
                id=h.id,
                ligne_id=h.ligne_id,
                destination=h.destination,
                heure_depart=h.heure_depart,
                heure_arrivee=h.heure_arrivee,
                station=h.station,
                quai=h.quai
            ) for h in horaires
        ]
    )
