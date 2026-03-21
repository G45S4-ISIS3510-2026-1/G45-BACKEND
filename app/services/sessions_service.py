# app/services/session_service.py

from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from app.models.sessions import Session
from app.models.enums import SessionStatus
from app.repositories.sessions_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.skills_service import SkillService


# Mapa de weekday() de Python (0=lunes) al campo de Availability
WEEKDAY_TO_FIELD = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
}


class SessionService:

    def __init__(self, session_repo: SessionRepository, user_repo: UserRepository, skill_service: SkillService):
        self.session_repo = session_repo
        self.user_repo    = user_repo
        self.skill_service = skill_service

    # ------------------------------------------------------------------ HELPERS

    async def _assert_no_overlap(self, user_id: str, scheduled_at: datetime, exclude_session_id: str | None = None):
        """
        Verifica que el usuario no tenga ninguna sesión PENDIENTE
        dentro de una ventana de ±1 hora respecto a scheduled_at.
        """
        sessions = await self.session_repo.get_by_student(user_id)
        sessions += await self.session_repo.get_by_tutor(user_id)

        window_start = scheduled_at - timedelta(hours=1)
        window_end   = scheduled_at + timedelta(hours=1)

        for s in sessions:
            if exclude_session_id and s.id == exclude_session_id:
                continue
            if s.status != SessionStatus.PENDIENTE:
                continue
            if window_start < s.scheduled_at < window_end:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"El usuario '{user_id}' ya tiene una sesión reservada "
                        f"el {s.scheduled_at.strftime('%Y-%m-%d %H:%M')} UTC, "
                        f"lo cual entra en conflicto con la hora solicitada."
                    )
                )

    def _assert_within_availability(self, tutor, scheduled_at: datetime):
        """
        Verifica que la hora de scheduled_at esté presente en la
        disponibilidad del tutor para ese día de la semana.
        La comparación se hace solo sobre hora y minuto (ignora fecha).
        """
        weekday = scheduled_at.weekday()

        if weekday == 6:  # domingo no existe en availability
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pueden agendar sesiones los domingos."
            )

        day_field    = WEEKDAY_TO_FIELD[weekday]
        available_slots: list[datetime] = getattr(tutor.availability, day_field)

        if not available_slots:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El tutor no tiene disponibilidad el {day_field.capitalize()}."
            )

        # Comparar solo HH:MM ignorando fecha y timezone del slot almacenado
        requested_time = (scheduled_at.hour, scheduled_at.minute)
        available_times = {(slot.hour, slot.minute) for slot in available_slots}

        if requested_time not in available_times:
            slots_str = ", ".join(
                f"{slot.hour:02d}:{slot.minute:02d}" for slot in sorted(available_slots)
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"La hora {scheduled_at.strftime('%H:%M')} no está en la disponibilidad "
                    f"del tutor para el {day_field.capitalize()}. "
                    f"Horas disponibles: {slots_str}."
                )
            )

    # ------------------------------------------------------------------ CREATE
    async def create(self, session: Session) -> Session:
        # 1. Validar que la fecha no sea en el pasado
        now = datetime.now(timezone.utc)
        scheduled = session.scheduled_at
        if scheduled.tzinfo is None:
            scheduled = scheduled.replace(tzinfo=timezone.utc)
        if scheduled <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de la sesión debe ser en el futuro."
            )

        # 2. Validar existencia del estudiante
        student = await self.user_repo.get_by_id(session.student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante '{session.student_id}' no encontrado."
            )

        # 3. Validar existencia del tutor y que isTutoring sea True
        tutor = await self.user_repo.get_by_id(session.tutor_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor '{session.tutor_id}' no encontrado."
            )
        if not tutor.is_tutoring:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario '{session.tutor_id}' no está activo como tutor."
            )

        # 4. Estudiante y tutor no pueden ser el mismo usuario
        if session.student_id == session.tutor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un usuario no puede agendarse una tutoría consigo mismo."
            )

        # 5. Verificar disponibilidad horaria del tutor para ese día
        self._assert_within_availability(tutor, scheduled)

        # 6. Verificar que ni el estudiante ni el tutor tengan solapamiento de ±1h
        await self._assert_no_overlap(session.student_id, scheduled)
        await self._assert_no_overlap(session.tutor_id,   scheduled)
        
        print(f"debug: Validating skill existence for ID: {session.skill.id}")
        skill = await self.skill_service.get_by_id(session.skill.id)
        if not skill:
            print(f"debug: Skill {session.skill.id} NOT FOUND")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El skill '{session.skill.id}' no existe."
            )
        print(f"debug: Skill {session.skill.id} found")

        return await self.session_repo.create(session)

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, session_id: str) -> Session:
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sesión '{session_id}' no encontrada."
            )
        return session

    async def get_by_student(self, student_id: str) -> list[Session]:
        if not await self.user_repo.get_by_id(student_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante '{student_id}' no encontrado."
            )
        return await self.session_repo.get_by_student(student_id)

    async def get_by_tutor(self, tutor_id: str) -> list[Session]:
        if not await self.user_repo.get_by_id(tutor_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor '{tutor_id}' no encontrado."
            )
        return await self.session_repo.get_by_tutor(tutor_id)

    async def get_by_student_and_status(
        self, student_id: str, status_filter: SessionStatus
    ) -> list[Session]:
        if not await self.user_repo.get_by_id(student_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante '{student_id}' no encontrado."
            )
        return await self.session_repo.get_by_student_and_status(student_id, status_filter)

    async def get_by_tutor_and_status(
        self, tutor_id: str, status_filter: SessionStatus
    ) -> list[Session]:
        if not await self.user_repo.get_by_id(tutor_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor '{tutor_id}' no encontrado."
            )
        return await self.session_repo.get_by_tutor_and_status(tutor_id, status_filter)

    async def get_sessions_between(self, student_id: str, tutor_id: str) -> list[Session]:
        if not await self.user_repo.get_by_id(student_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante '{student_id}' no encontrado."
            )
        if not await self.user_repo.get_by_id(tutor_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor '{tutor_id}' no encontrado."
            )
        return await self.session_repo.get_session_between(student_id, tutor_id)

    # ------------------------------------------------------------------ UPDATE
    # app/services/session_service.py — reemplaza update_status por estos dos métodos

    # ------------------------------------------------------------------ UPDATE

    async def cancel(self, session_id: str) -> Session:
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sesión '{session_id}' no encontrada."
            )
        if session.status != SessionStatus.PENDIENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Solo se pueden cancelar sesiones en estado Pendiente. "
                       f"Estado actual: '{session.status.value}'."
            )
        return await self.session_repo.update_status(session_id, SessionStatus.CANCELADA)

    async def confirm(self, session_id: str, verif_code: str) -> Session:
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sesión '{session_id}' no encontrada."
            )
        if session.status != SessionStatus.PENDIENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Solo se pueden confirmar sesiones en estado Pendiente. "
                       f"Estado actual: '{session.status.value}'."
            )
        if session.verif_code != verif_code:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Código de verificación incorrecto."
            )
        return await self.session_repo.update_status(session_id, SessionStatus.EN_REVISION)


    # ------------------------------------------------------------------ DELETE
    async def delete(self, session_id: str) -> bool:
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sesión '{session_id}' no encontrada."
            )
        if session.status not in {SessionStatus.CANCELADA, SessionStatus.PENDIENTE}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar sesiones en estado Pendiente o Cancelada."
            )
        return await self.session_repo.delete(session_id)
