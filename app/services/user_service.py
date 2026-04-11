# app/services/user_service.py

from fastapi import HTTPException, status
from app.models.user import User, Availability, PaymentMethod
from app.models.enums import UniandesMajor
from app.repositories.user_repository import UserRepository

from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError
from app.models.notification import NotificationPayload


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    # ------------------------------------------------------------------ CREATE
    async def register(self, user: User) -> User:
        if await self.repo.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario registrado con el correo '{user.email}'."
            )
        return await self.repo.create(user)

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, user_id: str) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        return user

    async def get_by_email(self, email: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con correo '{email}' no encontrado."
            )
        return user

    async def get_all(self) -> list[User]:
        return await self.repo.get_all()

    async def get_all_tutors(self) -> list[User]:
        return await self.repo.get_all_tutors()

    async def search_tutors(
        self,
        name: str | None = None,
        skill_ids: list[str] | None = None,
        major: UniandesMajor | None = None,
    ) -> list[User]:
        """
        Búsqueda filtrada de tutores. Los filtros son acumulativos (AND):
        - name:      substring case-insensitive sobre el campo 'name'
        - skill_ids: al menos uno de los IDs debe estar en tutoringSkills
        - major:     carrera exacta del tutor
        """
        if skill_ids:
            tutors = await self.repo.get_tutors_by_skills(skill_ids)
        else:
            tutors = await self.repo.get_all_tutors()

        if name:
            name_lower = name.strip().lower()
            tutors = [t for t in tutors if name_lower in t.name.lower()]

        if major:
            tutors = [t for t in tutors if t.major == major]

        return tutors

    # ------------------------------------------------------------------ UPDATE GENERAL
    async def update(self, user_id: str, user: User) -> User:
        existing = await self.repo.get_by_id(user_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        # Verificar conflicto de email si cambió
        if user.email != existing.email:
            if await self.repo.get_by_email(user.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El correo '{user.email}' ya está en uso por otro usuario."
                )
        # Verificar conflicto de uniandesId si cambió
        if user.uniandes_id != existing.uniandes_id:
            if await self.repo.get_by_uniandes_id(user.uniandes_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El ID Uniandes '{user.uniandes_id}' ya está en uso por otro usuario."
                )
        return await self.repo.update(user_id, user)

    # ------------------------------------------------------------------ UPDATE ESPECÍFICOS

    async def set_tutoring(self, user_id: str, is_tutoring: bool) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if user.is_tutoring == is_tutoring:
            state = "tutor" if is_tutoring else "estudiante"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El usuario ya se encuentra en modo {state}."
            )
        return await self.repo.set_tutoring(user_id, is_tutoring)

    async def update_availability(self, user_id: str, availability: Availability) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if not user.is_tutoring:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo los tutores pueden modificar su disponibilidad."
            )
        return await self.repo.update_availability(user_id, availability)

    async def update_tutoring_skills(self, user_id: str, skill_ids: list[str]) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if not user.is_tutoring:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo los tutores pueden definir skills de tutoría."
            )
        return await self.repo.update_tutoring_skills(user_id, skill_ids)

    async def update_interested_skills(self, user_id: str, skill_ids: list[str]) -> User:
        if not await self.repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        return await self.repo.update_interested_skills(user_id, skill_ids)

    async def update_fav_tutors(self, user_id: str, fav_tutor_ids: list[str]) -> User:
        if not await self.repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        # Verificar que todos los IDs referenciados existen y son tutores
        for tutor_id in fav_tutor_ids:
            tutor = await self.repo.get_by_id(tutor_id)
            if not tutor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El tutor '{tutor_id}' no existe."
                )
            if not tutor.is_tutoring:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El usuario '{tutor_id}' no es tutor."
                )
        return await self.repo.update_fav_tutors(user_id, fav_tutor_ids)

    # -------- Payment Methods

    async def add_payment_method(self, user_id: str, method: PaymentMethod) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if len(user.payment_methods) >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pueden registrar más de 3 métodos de pago."
            )
        duplicate = any(m.number == method.number for m in user.payment_methods)
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El número de tarjeta '{method.number}' ya está registrado."
            )
        return await self.repo.add_payment_method(user_id, method)

    async def remove_payment_method(self, user_id: str, card_number: str) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if not any(m.number == card_number for m in user.payment_methods):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró una tarjeta con número '{card_number}'."
            )
        return await self.repo.remove_payment_method(user_id, card_number)

    # -------- FCM Tokens / Sesión de dispositivo

    async def login(self, user_id: str, fcm_token: str) -> User:
        """Registra el token FCM del dispositivo al iniciar sesión."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if fcm_token in user.fcm_tokens:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El dispositivo ya tiene una sesión activa."
            )
        return await self.repo.add_fcm_token(user_id, fcm_token)

    async def logout(self, user_id: str, fcm_token: str) -> User:
        """Elimina el token FCM del dispositivo al cerrar sesión."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if fcm_token not in user.fcm_tokens:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El token FCM no corresponde a ninguna sesión activa."
            )
        return await self.repo.remove_fcm_token(user_id, fcm_token)

    # ------------------------------------------------------------------ DELETE
    async def delete(self, user_id: str) -> bool:
        if not await self.repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        return await self.repo.delete(user_id)

    # ------------------------------------------------------------------ NOTIFICATIONS

    async def send_push_notification(
        self,
        user_id: str,
        payload: NotificationPayload
    ) -> dict:
        """
        Envía una notificación push a todos los dispositivos activos del usuario.
        Usa MulticastMessage para enviar a todos sus fcmTokens en una sola llamada.
        Limpia automáticamente los tokens inválidos o expirados del documento.
        """
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if not user.fcm_tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene dispositivos con sesión activa."
            )

        message = messaging.MulticastMessage(
            tokens=user.fcm_tokens,
            notification=messaging.Notification(
                title=payload.title,
                body=payload.body,
            ),
            data=payload.data or {},
        )

        try:
            batch_response: messaging.BatchResponse = (
                await messaging.send_each_for_multicast_async(message)
            )
        except FirebaseError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error al comunicarse con FCM: {str(e)}"
            )

        # Identificar y limpiar tokens inválidos/expirados
        invalid_tokens = [
            user.fcm_tokens[i]
            for i, resp in enumerate(batch_response.responses)
            if not resp.success
            and resp.exception
            and "invalid-registration-token" in str(resp.exception).lower()
            or "registration-token-not-registered" in str(resp.exception).lower()
        ]
        for token in invalid_tokens:
            await self.repo.remove_fcm_token(user_id, token)

        return {
            "success_count": batch_response.success_count,
            "failure_count": batch_response.failure_count,
            "removed_tokens": invalid_tokens,
        }
    
    # ------------------------------------------------------------------ SESSION PRICE

    async def update_session_price(self, user_id: str, new_price: int) -> User:
        tutor = await self.repo.get_by_id(user_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if not tutor.is_tutoring:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo los tutores pueden tener un precio de sesión."
            )
        if new_price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio no puede ser negativo."
            )
        if new_price == tutor.session_price:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El precio ya es {new_price} COP."
            )

        # Actualizar el precio
        updated_tutor = await self.repo.update(
            user_id,
            tutor.model_copy(update={"session_price": new_price})
        )

        # Notificar a todos los usuarios que tienen a este tutor como favorito
        fans = await self.repo.get_users_with_fav_tutor(user_id)
        price_label = f"{'Gratis' if new_price == 0 else f'{new_price:,} COP'}"
        payload = NotificationPayload(
            title=f"{tutor.name} actualizó su precio",
            body=f"Las sesiones con {tutor.name} ahora cuestan {price_label}.",
            data={
                "type":    "TUTOR_PRICE_UPDATED",
                "tutorId": user_id,
                "price":   str(new_price),
            }
        )
        for fan in fans:
            if fan.fcm_tokens:
                try:
                    await self.send_push_notification(fan.id, payload)
                except HTTPException:
                    pass  # No interrumpir si un usuario no tiene tokens activos

        return updated_tutor
    
    async def update_profile_image(self, user_id: str, image_url: str) -> User:
        """Actualiza la URL de la imagen de perfil del usuario."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{user_id}' no encontrado."
            )
        if not image_url.startswith(("http://", "https://")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La URL de la imagen debe comenzar con http:// o https://"
            )
        
        return await self.repo.update(
            user_id,
            user.model_copy(update={"profile_image_url": image_url})
        )
