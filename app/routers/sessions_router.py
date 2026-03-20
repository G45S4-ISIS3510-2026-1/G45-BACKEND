# app/routers/session_router.py

from typing import List

from fastapi import APIRouter, Depends, Query
from app.models.sessions import Session
from app.models.enums import SessionStatus
from app.services.sessions_service import SessionService

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# ------------------------------------------------------------------ Dependencias

from app.dependencies import (
    get_session_service
)

SS = Depends(get_session_service)


# ------------------------------------------------------------------ CREATE

@router.post("/", response_model=Session, status_code=201)
async def create_session(session: Session, svc: SessionService = SS):
    return await svc.create(session)


# ------------------------------------------------------------------ READ

@router.get("/{session_id}", response_model=Session)
async def get_by_id(session_id: str, svc: SessionService = SS):
    return await svc.get_by_id(session_id)

@router.get("/", response_model=list[Session])
async def get_all(svc: SessionService = SS):
    return await svc.get_all()

@router.get("/by-student/{student_id}", response_model=list[Session])
async def get_by_student(
    student_id:    str,
    status_filter: SessionStatus | None = Query(default=None, description="Filtrar por estado"),
    svc:           SessionService = SS,
):
    if status_filter:
        return await svc.get_by_student_and_status(student_id, status_filter)
    return await svc.get_by_student(student_id)

@router.get("/by-tutor/{tutor_id}", response_model=list[Session])
async def get_by_tutor(
    tutor_id:      str,
    status_filter: SessionStatus | None = Query(default=None, description="Filtrar por estado"),
    svc:           SessionService = SS,
):
    if status_filter:
        return await svc.get_by_tutor_and_status(tutor_id, status_filter)
    return await svc.get_by_tutor(tutor_id)

@router.get("/between/{student_id}/{tutor_id}", response_model=list[Session])
async def get_sessions_between(student_id: str, tutor_id: str, svc: SessionService = SS):
    return await svc.get_sessions_between(student_id, tutor_id)


# ------------------------------------------------------------------ UPDATE

@router.patch("/{session_id}/cancel", response_model=Session)
async def cancel_session(session_id: str, svc: SessionService = SS):
    return await svc.cancel(session_id)

@router.patch("/{session_id}/confirm", response_model=Session)
async def confirm_session(
    session_id:  str,
    verif_code:  str = Query(..., description="Código alfanumérico de verificación de la sesión"),
    svc:         SessionService = SS,
):
    return await svc.confirm(session_id, verif_code)


# ------------------------------------------------------------------ DELETE

@router.delete("/{session_id}", status_code=204)
async def delete_session(session_id: str, svc: SessionService = SS):
    await svc.delete(session_id)
