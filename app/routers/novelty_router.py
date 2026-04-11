# app/routers/novelties_router.py

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/novelties", tags=["Novelties"])

# ------------------------------------------------------------------ Dependencias
from app.dependencies import (
    get_novelty_service
)

NS = Depends(get_novelty_service)

# ------------------------------- Marcar como leido

@router.patch("/{novelty_id}/mark-read", response_model=bool, status_code=200)
async def mark_as_read(novelty_id: str, svc = NS):
    return await svc.mark_as_read(novelty_id)