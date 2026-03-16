# app/routers/pqr_router.py

from fastapi import APIRouter, Depends, Query
from app.models.pqrs import PQR
from app.models.enums import SessionStatus, PQRType
from app.services.pqrs_service import PQRService

router = APIRouter(prefix="/pqrs", tags=["PQRs"])


# ------------------------------------------------------------------ Dependencias

from app.dependencies import (
    get_pqr_service
)

PS = Depends(get_pqr_service)


# ------------------------------------------------------------------ CREATE

@router.post("/", response_model=PQR, status_code=201)
async def create_pqr(pqr: PQR, svc: PQRService = PS):
    return await svc.create(pqr)


# ------------------------------------------------------------------ READ

@router.get("/by-status", response_model=list[PQR])
async def get_by_status(
    status_filter: SessionStatus = Query(..., description="Estado del PQR"),
    svc:           PQRService = PS,
):
    return await svc.get_by_status(status_filter)

@router.get("/by-type", response_model=list[PQR])
async def get_by_type(
    pqr_type: PQRType = Query(..., description="Tipo de PQR: Queja, Reclamo o Petición"),
    svc:      PQRService = PS,
):
    return await svc.get_by_type(pqr_type)

@router.get("/by-author/{author_id}", response_model=list[PQR])
async def get_by_author(author_id: str, svc: PQRService = PS):
    return await svc.get_by_author(author_id)

@router.get("/by-session/{session_id}", response_model=list[PQR])
async def get_by_related_incident(session_id: str, svc: PQRService = PS):
    return await svc.get_by_related_incident(session_id)

@router.get("/{pqr_id}", response_model=PQR)
async def get_by_id(pqr_id: str, svc: PQRService = PS):
    return await svc.get_by_id(pqr_id)


# ------------------------------------------------------------------ UPDATE

@router.patch("/{pqr_id}/review", response_model=PQR)
async def mark_in_review(pqr_id: str, svc: PQRService = PS):
    return await svc.mark_in_review(pqr_id)

@router.patch("/{pqr_id}/resolve", response_model=PQR)
async def resolve_pqr(pqr_id: str, svc: PQRService = PS):
    return await svc.resolve(pqr_id)

@router.patch("/{pqr_id}/cancel", response_model=PQR)
async def cancel_pqr(pqr_id: str, svc: PQRService = PS):
    return await svc.cancel(pqr_id)


# ------------------------------------------------------------------ DELETE

@router.delete("/{pqr_id}/by/{requesting_user_id}", status_code=204)
async def delete_pqr(pqr_id: str, requesting_user_id: str, svc: PQRService = PS):
    await svc.delete(pqr_id, requesting_user_id)
