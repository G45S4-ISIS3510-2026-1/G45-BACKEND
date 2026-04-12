# app/routers/session_router.py

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

@router.get("/by-student/{student_id}", response_model=list[Session])
async def get_by_student(
    student_id:    str,
    svc:           SessionService = SS,
):
    return await svc.get_by_student(student_id)

@router.get("/by-tutor/{tutor_id}", response_model=list[Session])
async def get_by_tutor(
    tutor_id:      str,
    svc:           SessionService = SS,
):
    return await svc.get_by_tutor(tutor_id)

@router.get("/between/{tutor_id}/{student_id}", response_model=list[Session])
async def get_between_tutor_and_student(
    tutor_id:     str,
    student_id:   str,
    svc:           SessionService = SS,
):
    return await svc.get_by_tutor_and_student(tutor_id, student_id)

@router.get("/upcoming/{user_id}", response_model=list[Session])
async def get_upcoming_sessions_for_user(
    user_id:      str,
    svc:           SessionService = SS,
):
    # return await svc.get_upcoming_sessions_for_user(user_id)
    return

@router.get("/previous/{user_id}", response_model=list[Session])
async def get_previous_sessions_for_user(
    user_id:      str,
    svc:           SessionService = SS,
):
    #return await svc.get_previous_sessions_for_user(user_id)
    return
# ------------------------------------------------------------------ UPDATE

@router.patch("/{session_id}/{participant_id}/cancel", response_model=Session)
async def cancel_session(session_id: str, participant_id: str, svc: SessionService = SS):
    return await svc.cancel(session_id, participant_id)

@router.patch("/{session_id}/confirm", response_model=Session)
async def confirm_session(
    session_id:  str,
    verif_code:  str = Query(..., description="Código alfanumérico de verificación de la sesión"),
    svc:         SessionService = SS,
):
    return await svc.confirm(session_id, verif_code)
