# app/routers/user_router.py

from fastapi import APIRouter, Query
from app.models.user import User, Availability, PaymentMethod
from app.models.notification import NotificationPayload
from app.models.enums import UniandesMajor
from app.services.user_service import UserService
from app.services.reviews_service import ReviewService
from app.dtos.tutor_summary import TutorSummary

router = APIRouter(prefix="/users", tags=["Users"])


# ------------------------------------------------------------------ Dependencias
# Se asume inyección de dependencias configurada en main.py
# Ejemplo de uso: get_user_service() -> UserService

from app.dependencies import (
    get_user_service
)

from fastapi import Depends
US = Depends(get_user_service)


# ------------------------------------------------------------------ CREATE

@router.post("/", response_model=User, status_code=201)
async def register(user: User, svc: UserService = US):
    return await svc.register(user)


# ------------------------------------------------------------------ READ

@router.get("/profile/{user_id}", response_model=User)
async def get_by_id(user_id: str, svc: UserService = US):
    return await svc.get_user_by_id(user_id)

@router.get("/tutor/{user_id}", response_model=User)
async def get_tutor_by_id(user_id: str, svc: UserService = US):
    return await svc.get_tutor_by_id(user_id)


@router.get("/tutors/search", response_model=list[TutorSummary])
async def search_tutors(
    name:      str | None       = Query(default=None, description="Substring del nombre del tutor"),
    skill_ids: list[str] | None = Query(default=None, description="IDs de skills (al menos uno debe coincidir)"),
    major:     UniandesMajor | None = Query(default=None, description="Carrera del tutor"),
    min_rating: float | None = Query(default=None, ge=0, le=5, description="Calificación mínima promedio del tutor"),
    min_price: int | None = Query(default=None, ge=0, description="Precio mínimo por sesión"),
    max_price: int | None = Query(default=None, ge=0, description="Precio máximo por sesión"),
    limit: int = Query(default=20, ge=1, le=100, description="Número máximo de resultados a retornar"),
    svc:       UserService  = US
):
    tutors = await svc.search_tutors(name=name, skill_ids=skill_ids, major=major, min_rating=min_rating, min_price=min_price, max_price=max_price, limit=limit)
    summaries = []
    for tutor in tutors:
        summaries.append(TutorSummary(
            id=tutor.id,
            name=tutor.name,
            major=tutor.major,
            rating=tutor.tutorRating,
            profile_image_url=tutor.profile_image_url,
            session_price=tutor.session_price,    
        ))
    return summaries

#para FLUTTER
@router.get("/by-email/{email}", response_model=User)
async def get_user_by_email(email: str, svc: UserService = US):
    return await svc.get_user_by_email(email)


# ------------------------------------------------------------------ UPDATE GENERAL

@router.put("/{user_id}", response_model=User)
async def update(user_id: str, user: User, svc: UserService = US):
    return await svc.update(user_id, user)


# ------------------------------------------------------------------ UPDATE ESPECÍFICOS

@router.patch("/{user_id}/tutoring", response_model=User)
async def set_tutoring(
    user_id:     str,
    is_tutoring: bool = Query(..., description="True para activar modo tutor, False para desactivar"),
    svc:         UserService = US,
):
    return await svc.set_tutoring(user_id, is_tutoring)

@router.patch("/{user_id}/availability", response_model=User)
async def update_availability(user_id: str, availability: Availability, svc: UserService = US):
    return await svc.update_availability(user_id, availability)

@router.patch("/{user_id}/tutoring-skills", response_model=User)
async def update_tutoring_skills(user_id: str, skill_ids: list[str], svc: UserService = US):
    return await svc.update_tutoring_skills(user_id, skill_ids)

@router.patch("/{user_id}/interested-skills", response_model=User)
async def update_interested_skills(user_id: str, skill_ids: list[str], svc: UserService = US):
    return await svc.update_interested_skills(user_id, skill_ids)

@router.patch("/{user_id}/fav-tutors", response_model=User)
async def update_fav_tutors(user_id: str, fav_tutor_ids: list[str], svc: UserService = US):
    return await svc.update_fav_tutors(user_id, fav_tutor_ids)


@router.patch("/{user_id}/session-price", response_model=User)
async def update_session_price(
    user_id:   str,
    new_price: int = Query(..., ge=0, description="Nuevo precio en pesos colombianos"),
    svc:       UserService = US,
):
    return await svc.update_session_price(user_id, new_price)


@router.patch("/{user_id}/profile-image", response_model=User)
async def update_profile_image(
    user_id:   str,
    image_url: str = Query(..., description="Nueva URL de la imagen de perfil"),
    svc:       UserService = US,
):
    return await svc.update_profile_image(user_id, image_url)




# -------- Payment Methods

@router.post("/{user_id}/payment-methods", response_model=User)
async def add_payment_method(user_id: str, method: PaymentMethod, svc: UserService = US):
    return await svc.add_payment_method(user_id, method)

@router.delete("/{user_id}/payment-methods/{card_number}", response_model=User)
async def remove_payment_method(user_id: str, card_number: str, svc: UserService = US):
    return await svc.remove_payment_method(user_id, card_number)


# -------- Sesión de dispositivo

@router.post("/{user_id}/login", response_model=User)
async def login(
    user_id:   str,
    fcm_token: str = Query(..., description="Token FCM del dispositivo"),
    svc:       UserService = US,
):
    return await svc.login(user_id, fcm_token)

@router.post("/{user_id}/logout", response_model=User)
async def logout(
    user_id:   str,
    fcm_token: str = Query(..., description="Token FCM del dispositivo a cerrar"),
    svc:       UserService = US,
):
    return await svc.logout(user_id, fcm_token)


# -------- Notificaciones push

@router.post("/{user_id}/notify", response_model=dict)
async def send_notification(user_id: str, payload: NotificationPayload, svc: UserService = US):
    return await svc.send_push_notification(user_id, payload)


# ------------------------------------------------------------------ DELETE

@router.delete("/{user_id}", status_code=204)
async def delete(user_id: str, svc: UserService = US):
    await svc.delete(user_id)

