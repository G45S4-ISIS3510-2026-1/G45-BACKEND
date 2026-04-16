from apscheduler.schedulers.blocking import BlockingScheduler
from firebase_admin import messaging

from app.core.firebase import get_firestore_client
from app.models.enums import NoveltyType
from app.models.novelty import Novelty
from app.repositories.novelty_repository import NoveltiesRepository
from app.repositories.user_repository import UserRepository
async def health_check():
    db           = get_firestore_client()
    user_repo    = UserRepository(db)
    novelty_repo= NoveltiesRepository(db)
    print("Executing task/notification every 5 minutes...")
    users= await user_repo.get_all()
    novelty=Novelty(
        title="Health Check",
        description="This is a periodic health check notification.",
        user_id="system",
        type=NoveltyType.HEALTH_CHECK
    )
    await novelty_repo.create_novelty(novelty)
    
    for user in users:
        if user.fcm_tokens:
            message = messaging.MulticastMessage(
                tokens=user.fcm_tokens,
                notification=messaging.Notification(
                    title="Health Check",
                    body="This is a periodic health check notification.",
                ),
                data={"type": NoveltyType.HEALTH_CHECK},
            )
            try:
                messaging.send_each_for_multicast(message)
            except Exception as e:
                print(f"Error sending health check to user {user.id}: {e}")

