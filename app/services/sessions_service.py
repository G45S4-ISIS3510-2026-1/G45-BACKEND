# app/services/session_service.py

from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from app.core.currentWeekManager import getColombiaTimezone
from app.models.notification import NotificationPayload
from app.models.sessions import Session
from app.models.enums import SessionStatus
from app.repositories.sessions_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.services.skills_service import SkillService
from app.repositories.skills_repository import SkillRepository
from app.services.user_service import UserService


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

    def __init__(self, session_repo: SessionRepository, user_repo: UserRepository, skill_repo: SkillRepository, user_service:UserService):
        self.session_repo = session_repo
        self.user_repo    = user_repo
        self.skill_repo = skill_repo
        self.user_service = user_service
    # ------------------------------------------------------------------ HELPERS

    async def _assert_no_overlap(self, user_id: str, scheduled_at: datetime, exclude_session_id: str | None = None):
        """
        Verifica que el usuario no tenga ninguna sesión PENDIENTE
        dentro de una ventana de +1 hora respecto a scheduled_at.
        """
        sessions = await self.session_repo.get_by_student(user_id)
        sessions += await self.session_repo.get_by_tutor(user_id)

        window_start = scheduled_at
        window_end   = scheduled_at + timedelta(hours=1)

        for s in sessions:
            if exclude_session_id and s.id == exclude_session_id:
                continue
            if s.status != SessionStatus.PENDIENTE:
                continue
            if window_start <= s.scheduled_at < window_end:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"El usuario '{user_id}' ya tiene una sesión reservada/agendada "
                        f"el {s.scheduled_at.strftime('%Y-%m-%d %H:%M')}, "
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
        colombiaTimezone= getColombiaTimezone()
        now = datetime.now(colombiaTimezone)
        scheduled = session.scheduled_at
        if scheduled.tzinfo is None or scheduled.tzinfo != colombiaTimezone:
            correction= scheduled.replace(tzinfo=None)
            scheduled = correction.replace(tzinfo=colombiaTimezone)
        if scheduled <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de la sesión debe ser en el futuro."
            )

        # 2. Validar existencia del estudiante
        student = await self.user_repo.get_by_id(session.student.id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante '{session.student.id}' no encontrado."
            )

        # 3. Validar existencia del tutor y que isTutoring sea True
        tutor = await self.user_repo.get_by_id(session.tutor.id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor '{session.tutor.id}' no encontrado."
            )
        if not tutor.is_tutoring:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario '{session.tutor.id}' no está activo como tutor."
            )

        # 4. Estudiante y tutor no pueden ser el mismo usuario
        if session.student.id == session.tutor.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un usuario no puede agendarse una tutoría consigo mismo."
            )

        # 5. Verificar disponibilidad horaria del tutor para ese día
        self._assert_within_availability(tutor, scheduled)

        # 6. Verificar que ni el estudiante ni el tutor tengan solapamiento de ±1h
        await self._assert_no_overlap(session.student.id, scheduled)
        await self._assert_no_overlap(session.tutor.id,   scheduled)
        
        if session.skill is not None:
            skill = await self.skill_repo.get_by_id(session.skill.id)
            if not skill:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El skill '{session.skill.id}' no existe."
                )
        self.user_service.send_push_notification(
            user_id=session.tutor.id,
            payload=NotificationPayload(
                title="Nueva sesión solicitada",
                body=f"El estudiante {student.name} ha solicitado una sesión para el {scheduled.strftime('%Y-%m-%d %H:%M')}.",
            )
        )
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
