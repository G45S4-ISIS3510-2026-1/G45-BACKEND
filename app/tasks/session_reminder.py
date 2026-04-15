# app/tasks/session_reminders.py

import asyncio
from datetime import datetime, timezone, timedelta
from app.core.currentWeekManager import getColombiaTimezone
from app.core.firebase import get_firestore_client
from app.models.novelty import Novelty
from app.models.sessions import Session
from app.repositories.novelty_repository import NoveltiesRepository
from app.repositories.sessions_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.models.notification import NotificationPayload
from app.models.enums import NoveltyType, SessionStatus


async def _notify_user(user_repo: UserRepository, novelty_repo: NoveltiesRepository, user_id: str, session:Session, label: str):
    """Envía notificación push a un usuario sobre su sesión próxima."""
    user = await user_repo.get_by_id(user_id)
    if not user or not user.fcm_tokens:
        return

    from firebase_admin import messaging
    scheduled_str = session.scheduled_at.astimezone(getColombiaTimezone()).strftime("%H:%M") if session.scheduled_at else "fecha desconocida"
    payload = NotificationPayload(
        title="Recordatorio de tutoría 📚",
        body=f"Hoy tienes una sesión como {label} a las {scheduled_str}. Revisa tus novedades para más detalles.",
        data={
            "type":      "SESSION_REMINDER",
            "sessionId": session.id,
            "role":      label,
        }
    )
    message = messaging.MulticastMessage(
        tokens=user.fcm_tokens,
        notification=messaging.Notification(
            title=payload.title,
            body=payload.body,
        ),
        data=payload.data,
    )
    
    novelty= Novelty (
        user_id=user_id,
        title="Recordatorio de tutoría",
        entity_id=session.id,
        type=NoveltyType.SESION,
        description=f"Hoy tienes tutoría como {label} con {session.tutor.name if label=="estudiante" else session.student.name} a las {scheduled_str}. No olvides prepararte y asistir puntualmente."
    )
    try:
        await novelty_repo.create_novelty(novelty)
        await messaging.send_each_for_multicast(message)
    except Exception:
        pass  # No interrumpir el job por fallos individuales


async def check_upcoming_sessions():
    """
    Job diario: notifica a estudiantes y tutores que tienen
    una sesión PENDIENTE dentro de las próximas 24 horas.
    """
    db           = get_firestore_client()
    session_repo = SessionRepository(db)
    user_repo    = UserRepository(db)
    novelty_repo   = NoveltiesRepository(db)

    now        = datetime.now(getColombiaTimezone())
    window_end = now + timedelta(hours=24)

    # Traer todas las sesiones pendientes
    # (Firestore no soporta range queries sobre timestamps con otros filtros,
    #  por lo que filtramos en Python tras traer las pendientes)
    pending = await session_repo.col \
        .where("status", "==", SessionStatus.PENDIENTE.value) \
        .get()

    notify_tasks = []
    for doc in pending:
        session_data = doc.to_dict()
        scheduled_at = session_data.get("scheduledAt")

        # Normalizar timezone si viene sin tzinfo de Firestore
        if scheduled_at and scheduled_at.tzinfo is None:
            scheduled_at = scheduled_at.replace(tzinfo=getColombiaTimezone())

        if scheduled_at and now <= scheduled_at <= window_end:
            from app.models.sessions import Session
            session = Session(id=doc.id, **session_data)

            notify_tasks.append(
                _notify_user(user_repo, novelty_repo, session.student.id, session, "estudiante")
            )
            notify_tasks.append(
                _notify_user(user_repo, novelty_repo, session.tutor.id, session, "tutor")
            )

    if notify_tasks:
        await asyncio.gather(*notify_tasks, return_exceptions=True)
