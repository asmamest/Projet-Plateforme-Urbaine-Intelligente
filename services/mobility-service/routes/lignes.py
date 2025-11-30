"""
Routes CRUD pour la gestion des lignes de transport
"""
from fastapi import APIRouter, HTTPException, Path, status
from typing import List
from services.ligne_service import LigneService
from schemas.ligne import LigneCreate, LigneUpdate, LigneResponse

router = APIRouter(prefix="/lignes", tags=["Lignes"])
service = LigneService()

@router.get("", response_model=List[LigneResponse], summary="Lister toutes les lignes")
async def get_lignes():
    """
    Récupère la liste complète de toutes les lignes de transport disponibles.
    """
    lignes = service.get_all_lignes()
    return [
        LigneResponse(
            id=l.id,
            numero=l.numero,
            nom=l.nom,
            type_transport=l.type_transport.value,
            terminus_debut=l.terminus_debut,
            terminus_fin=l.terminus_fin,
            actif=l.actif,
            created_at=l.created_at,
            updated_at=l.updated_at
        ) for l in lignes
    ]

@router.post("", response_model=LigneResponse, status_code=status.HTTP_201_CREATED, summary="Créer une nouvelle ligne")
async def create_ligne(ligne_data: LigneCreate):
    """
    Crée une nouvelle ligne de transport dans le système.
    
    - **numero**: Numéro unique de la ligne (ex: L1, B15)
    - **nom**: Nom descriptif de la ligne
    - **type_transport**: Type de véhicule (bus, metro, train, tramway)
    - **terminus_debut**: Station de départ
    - **terminus_fin**: Station d'arrivée
    """
    ligne = service.create_ligne(ligne_data)
    return LigneResponse(
        id=ligne.id,
        numero=ligne.numero,
        nom=ligne.nom,
        type_transport=ligne.type_transport.value,
        terminus_debut=ligne.terminus_debut,
        terminus_fin=ligne.terminus_fin,
        actif=ligne.actif,
        created_at=ligne.created_at,
        updated_at=ligne.updated_at
    )

@router.put("/{id}", response_model=LigneResponse, summary="Mettre à jour une ligne")
async def update_ligne(
    id: str = Path(..., description="Identifiant de la ligne"),
    ligne_data: LigneUpdate = ...
):
    """
    Met à jour les informations d'une ligne existante.
    
    Seuls les champs fournis seront mis à jour, les autres resteront inchangés.
    """
    ligne = service.update_ligne(id, ligne_data)
    if not ligne:
        raise HTTPException(
            status_code=404,
            detail=f"Ligne avec l'ID {id} introuvable"
        )
    
    return LigneResponse(
        id=ligne.id,
        numero=ligne.numero,
        nom=ligne.nom,
        type_transport=ligne.type_transport.value,
        terminus_debut=ligne.terminus_debut,
        terminus_fin=ligne.terminus_fin,
        actif=ligne.actif,
        created_at=ligne.created_at,
        updated_at=ligne.updated_at
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer une ligne")
async def delete_ligne(
    id: str = Path(..., description="Identifiant de la ligne à supprimer")
):
    """
    Supprime définitivement une ligne du système.
    
    **Attention**: Cette action est irréversible.
    """
    success = service.delete_ligne(id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Ligne avec l'ID {id} introuvable"
        )
    return None
