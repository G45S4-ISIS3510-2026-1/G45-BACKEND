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
async def notify_near_sessions():
    db           = get_firestore_client()
    novelty_repo= NoveltiesRepository(db)
    user_repo    = UserRepository(db)
    session_repo= SessionRepository(db)
    print("Cheking for near sessions every hour...")
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
            
        time_till_session= session_time - now if session_time else None
        
        if session.status == "PENDIENTE" and time_till_session <= timedelta(hours=1):
            tutor= await user_repo.get_by_id(session.tutor.id)
            
            student= await user_repo.get_by_id(session.student.id)
            
            novelty_tutor.user_id=session.tutor.id
            novelty_tutor.title="Recordatorio de sesión próxima"
            novelty_tutor.type=NoveltyType.SESION
            novelty_tutor.entity_id=session.id
            novelty_tutor.description=f"Tienes una sesión programada en menos de una hora a las {session_time.strftime('%H:%M')}. Preparate y no olvides confirmar la asistencia con {student.name}."
            await novelty_repo.create_novelty(novelty_tutor)
            
            novelty_user.user_id=session.student.id
            novelty_user.title="Recordatorio de sesión próxima"
            novelty_user.type=NoveltyType.SESION
            novelty_user.entity_id=session.id
            novelty_user.description=f"Tienes una sesión programada en menos de una hora a las {session_time.strftime('%H:%M')}. Preparate y no olvides confirmar la asistencia con {tutor.name}."
            await novelty_repo.create_novelty(novelty_user)
            
            
            if tutor and tutor.fcm_token:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Recordatorio de sesión próxima",
                        body=f"Tienes una sesión programada en menos de una hora a las {session_time.strftime('%H:%M')}. Preparate y no olvides confirmar la asistencia con {student.name}."
                    ),
                    token=tutor.fcm_token
                )
                messaging.send(message)
            if student and student.fcm_token:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Recordatorio de sesión próxima",
                        body=f"Tienes una sesión programada en menos de una hora a las {session_time.strftime('%H:%M')}. Preparate y no olvides confirmar la asistencia con {tutor.name}."
                    ),
                    token=student.fcm_token
                )
                messaging.send(message)
        
