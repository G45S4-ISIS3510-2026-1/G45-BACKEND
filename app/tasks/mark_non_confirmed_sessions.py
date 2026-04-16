from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from firebase_admin import messaging

from app.core.currentWeekManager import getColombiaTimezone
from app.core.currentWeekManager import getColombiaTimezone
from app.core.firebase import get_firestore_client
from app.models.enums import NoveltyType, SessionStatus
from app.models.novelty import Novelty
from app.repositories.novelty_repository import NoveltiesRepository
from app.repositories.sessions_repository import SessionRepository
from app.repositories.sessions_repository import SessionRepository
from app.repositories.user_repository import UserRepository
async def mark_non_confirmed_sessions():
    db           = get_firestore_client()
    novelty_repo= NoveltiesRepository(db)
    user_repo    = UserRepository(db)
    session_repo= SessionRepository(db)
    print("Cheking for non-confirmed sessions every hour...")
    novelty_tutor=Novelty(
        title="Health Check",
        description="This is a periodic health check notification.",
        user_id="system",
        type=NoveltyType.HEALTH_CHECK
    )
    novelty_user=Novelty(
        title="Health Check",
        description="This is a periodic health check notification.",
        user_id="system",
        type=NoveltyType.HEALTH_CHECK
    )
    sessions= await session_repo.get_all()
    now        = datetime.now(getColombiaTimezone())
    
    for session in sessions:
        session_time = session.scheduled_at
        
        if session_time and session_time.tzinfo is None:
            session_time = session_time.replace(tzinfo=getColombiaTimezone())
        
        if session.status == "PENDIENTE" and session_time and session_time+timedelta(hours=1) < now:
            session_repo.update_status(session.id, SessionStatus.VENCIDA)
            
            novelty_tutor.user_id=session.tutor.id
            novelty_tutor.title="Sesión vencida"
            novelty_tutor.type=NoveltyType.SESION
            novelty_tutor.entity_id=session.id
            novelty_tutor.description=f"Tú o tu estudiante no han confirmado la sesión programada para {session_time.strftime('%Y-%m-%d %H:%M')}, por lo que se ha marcado como vencida. Para mas ayuda, contacta al soporte mediante PQRS."
            await novelty_repo.create_novelty(novelty_tutor)
            
            novelty_user.user_id=session.student.id
            novelty_user.title="Sesión vencida"
            novelty_user.type=NoveltyType.SESION
            novelty_user.entity_id=session.id
            novelty_user.description=f"Tú o tu tutor no han confirmado la sesión programada para {session_time.strftime('%Y-%m-%d %H:%M')}, por lo que se ha marcado como vencida. Para mas ayuda, contacta al soporte mediante PQRS."
            await novelty_repo.create_novelty(novelty_user)
            
            tutor= await user_repo.get_by_id(session.tutor.id)
            if tutor and tutor.fcm_token:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Sesión vencida",
                        body=f"Tú o tu estudiante no han confirmado la sesión programada para {session_time.strftime('%Y-%m-%d %H:%M')}, por lo que se ha marcado como vencida."
                    ),
                    token=tutor.fcm_token
                )
                messaging.send(message)
            student= await user_repo.get_by_id(session.student.id)
            if student and student.fcm_token:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Sesión vencida",
                        body=f"Tú o tu tutor no han confirmado la sesión programada para {session_time.strftime('%Y-%m-%d %H:%M')}, por lo que se ha marcado como vencida."
                    ),
                    token=student.fcm_token
                )
                messaging.send(message)
        
