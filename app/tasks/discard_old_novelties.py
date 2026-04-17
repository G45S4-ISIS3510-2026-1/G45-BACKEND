from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from firebase_admin import messaging

from app.core.currentWeekManager import getColombiaTimezone
from app.core.firebase import get_firestore_client
from app.models.novelty import Novelty
from app.repositories.novelty_repository import NoveltiesRepository
async def old_novelties():
    db           = get_firestore_client()
    novelty_repo= NoveltiesRepository(db)
    print("Checking old novelties every day.")
    novelties=await novelty_repo.get_all()
    
    now=datetime.now(getColombiaTimezone())
    
    for novelty in novelties:
        novelty_time=novelty.created_at
        
        if novelty_time and novelty_time.tzinfo is None:
            novelty_time = novelty_time.replace(tzinfo=getColombiaTimezone())
        
        if novelty_time and (now - novelty_time).days >= 7:
            await novelty_repo.mark_as_read(novelty.id)
            print(f"Marked old novelty as read with ID: {novelty.id}")
    
    

