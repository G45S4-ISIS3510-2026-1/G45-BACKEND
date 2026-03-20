# app/dependencies.py

from functools import lru_cache
from app.core.firebase import get_firestore_client

from app.repositories.user_repository    import UserRepository
from app.repositories.skills_repository   import SkillRepository
from app.repositories.reviews_repository  import ReviewRepository
from app.repositories.sessions_repository import SessionRepository
from app.repositories.pqrs_repository     import PQRRepository

from app.services.user_service    import UserService
from app.services.skills_service   import SkillService
from app.services.reviews_service  import ReviewService
from app.services.sessions_service import SessionService
from app.services.pqrs_service     import PQRService


# ------------------------------------------------------------------ Repositorios

def get_user_repo()    -> UserRepository:
    return UserRepository(get_firestore_client())

def get_skill_repo()   -> SkillRepository:
    return SkillRepository(get_firestore_client())

def get_review_repo()  -> ReviewRepository:
    return ReviewRepository(get_firestore_client())

def get_session_repo() -> SessionRepository:
    return SessionRepository(get_firestore_client())

def get_pqr_repo()     -> PQRRepository:
    return PQRRepository(get_firestore_client())


# ------------------------------------------------------------------ Servicios

def get_user_service() -> UserService:
    return UserService(get_user_repo())

def get_skill_service() -> SkillService:
    return SkillService(get_skill_repo())

def get_review_service() -> ReviewService:
    return ReviewService(get_review_repo(), get_user_repo())

def get_session_service() -> SessionService:
    return SessionService(get_session_repo(), get_user_repo(), get_skill_repo())

def get_pqr_service() -> PQRService:
    return PQRService(get_pqr_repo(), get_user_repo(), get_session_repo())
