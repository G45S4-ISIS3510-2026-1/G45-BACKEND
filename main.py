# main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.firebase import init_firebase
from app.routers.user_router    import router as user_router
from app.routers.skills_router   import router as skill_router
from app.routers.reviews_router  import router as review_router
from app.routers.sessions_router import router as session_router
from app.routers.pqrs_router     import router as pqr_router
from app.routers.novelty_router import router as novelty_router

from app.core.scheduler import scheduler, setup_scheduler
from app.tasks.session_reminder import check_upcoming_sessions
from app.core.config import settings
from app.mockData.seeder import seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase(settings.FIREBASE_CREDENTIALS_PATH)
    setup_scheduler([
        (check_upcoming_sessions, {"hour": 12, "minute": 0, "timezone": "America/Bogota"}),
    ])
    scheduler.start()

    if settings.APP_ENV == "development":
        from app.core.firebase import get_firestore_client
        await seed(get_firestore_client())

    yield

    scheduler.shutdown()


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(skill_router)
app.include_router(review_router)
app.include_router(session_router)
app.include_router(pqr_router)
app.include_router(novelty_router)
