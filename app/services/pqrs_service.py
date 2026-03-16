# app/services/pqr_service.py

from fastapi import HTTPException, status
from app.models.pqrs import PQR
from app.models.enums import SessionStatus, PQRType
from app.repositories.pqrs_repository import PQRRepository
from app.repositories.user_repository import UserRepository
from app.repositories.sessions_repository import SessionRepository


class PQRService:

    def __init__(
        self,
        pqr_repo:     PQRRepository,
        user_repo:    UserRepository,
        session_repo: SessionRepository,
    ):
        self.pqr_repo     = pqr_repo
        self.user_repo    = user_repo
        self.session_repo = session_repo

    # ------------------------------------------------------------------ CREATE
    async def create(self, pqr: PQR) -> PQR:
        # Validar existencia del autor
        if not await self.user_repo.get_by_id(pqr.author_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{pqr.author_id}' no encontrado."
            )

        # Validar sesión relacionada si fue proporcionada
        if pqr.related_incident:
            session = await self.session_repo.get_by_id(pqr.related_incident)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La sesión '{pqr.related_incident}' no existe."
                )
            # El autor debe ser participante de la sesión referenciada
            if pqr.author_id not in {session.student_id, session.tutor_id}:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="El autor no es participante de la sesión referenciada."
                )
            # Solo tiene sentido referenciar sesiones no pendientes
            if session.status == SessionStatus.PENDIENTE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede abrir un PQR sobre una sesión aún pendiente."
                )

        return await self.pqr_repo.create(pqr)

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, pqr_id: str) -> PQR:
        pqr = await self.pqr_repo.get_by_id(pqr_id)
        if not pqr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PQR '{pqr_id}' no encontrado."
            )
        return pqr

    async def get_by_author(self, author_id: str) -> list[PQR]:
        if not await self.user_repo.get_by_id(author_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{author_id}' no encontrado."
            )
        return await self.pqr_repo.get_by_author(author_id)

    async def get_by_status(self, status_filter: SessionStatus) -> list[PQR]:
        return await self.pqr_repo.get_by_status(status_filter)

    async def get_by_type(self, pqr_type: PQRType) -> list[PQR]:
        return await self.pqr_repo.get_by_type(pqr_type)

    async def get_by_related_incident(self, session_id: str) -> list[PQR]:
        if not await self.session_repo.get_by_id(session_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sesión '{session_id}' no encontrada."
            )
        return await self.pqr_repo.get_by_related_incident(session_id)

    # ------------------------------------------------------------------ UPDATE
    async def resolve(self, pqr_id: str) -> PQR:
        """Marca el PQR como Concluido (resolución favorable)."""
        return await self._transition(pqr_id, SessionStatus.CONCLUIDA)

    async def cancel(self, pqr_id: str) -> PQR:
        """Marca el PQR como Cancelado (desestimado o retirado)."""
        return await self._transition(pqr_id, SessionStatus.CANCELADA)

    async def mark_in_review(self, pqr_id: str) -> PQR:
        """Pasa el PQR a En Revisión para indicar que está siendo atendido."""
        return await self._transition(pqr_id, SessionStatus.EN_REVISION)

    async def _transition(self, pqr_id: str, new_status: SessionStatus) -> PQR:
        pqr = await self.pqr_repo.get_by_id(pqr_id)
        if not pqr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PQR '{pqr_id}' no encontrado."
            )
        allowed_transitions = {
            SessionStatus.PENDIENTE:   {SessionStatus.EN_REVISION, SessionStatus.CANCELADA},
            SessionStatus.EN_REVISION: {SessionStatus.CONCLUIDA,   SessionStatus.CANCELADA},
            SessionStatus.CONCLUIDA:   set(),
            SessionStatus.CANCELADA:   set(),
        }
        if new_status not in allowed_transitions[pqr.status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"No se puede cambiar el estado de '{pqr.status.value}' "
                    f"a '{new_status.value}'."
                )
            )
        return await self.pqr_repo.update_status(pqr_id, new_status)

    # ------------------------------------------------------------------ DELETE
    async def delete(self, pqr_id: str, requesting_user_id: str) -> bool:
        pqr = await self.pqr_repo.get_by_id(pqr_id)
        if not pqr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PQR '{pqr_id}' no encontrado."
            )
        if pqr.author_id != requesting_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el autor puede eliminar su PQR."
            )
        if pqr.status != SessionStatus.PENDIENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar PQRs en estado Pendiente."
            )
        return await self.pqr_repo.delete(pqr_id)
