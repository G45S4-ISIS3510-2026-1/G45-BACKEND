# app/repositories/user_repository.py

from google.cloud.firestore_v1 import AsyncClient, ArrayUnion, ArrayRemove
from app.models.user import User, Availability, PaymentMethod


COLLECTION = "users"


class UserRepository:

    def __init__(self, db: AsyncClient):
        self.db = db
        self.col = db.collection(COLLECTION)

    # ------------------------------------------------------------------ HELPERS
    def _doc_to_user(self, doc) -> User:
        data = doc.to_dict()
        data.pop("id", None)  # ← Remover "id" manualmente
        return User(id=doc.id, **data)

    # ------------------------------------------------------------------ CREATE
    async def create(self, user: User) -> User:
        if user.id is not None:
            doc_ref = self.col.document(user.id)
        else:
            doc_ref = self.col.document()
        data = user.model_dump(by_alias=True)
        await doc_ref.set(data)
        user.id = doc_ref.id
        return user

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, user_id: str) -> User | None:
        doc = await self.col.document(user_id).get()
        if not doc.exists:
            return None
        return self._doc_to_user(doc)

    async def get_by_email(self, email: str) -> User | None:
        docs = await self.col.where("email", "==", email).limit(1).get()
        if not docs:
            return None
        return self._doc_to_user(docs[0])

    async def get_by_uniandes_id(self, uniandes_id: int) -> User | None:
        docs = await self.col.where("uniandesId", "==", uniandes_id).limit(1).get()
        if not docs:
            return None
        return self._doc_to_user(docs[0])

    async def get_all(self) -> list[User]:
        docs = await self.col.get()
        return [self._doc_to_user(doc) for doc in docs]

    async def get_all_tutors(self) -> list[User]:
        docs = await self.col.where("isTutoring", "==", True).get()
        return [self._doc_to_user(doc) for doc in docs]

    async def get_tutors_by_skills(self, skill_ids: list[str]) -> list[User]:
        """
        Retorna tutores cuyo tutoringSkills tiene intersección
        con al menos uno de los skill_ids recibidos.
        Usa array-contains-any nativo de Firestore (máximo 30 valores).
        """
        skill_ids = list(set(skill_ids))  # deduplicar
        if not skill_ids:
            return []
        # array-contains-any soporta hasta 30 elementos
        docs = await (
            self.col
            .where("isTutoring", "==", True)
            .where("tutoringSkills", "array-contains-any", skill_ids[:30])
            .get()
        )
        return [self._doc_to_user(doc) for doc in docs]

    # ------------------------------------------------------------------ UPDATE GENERAL
    async def update(self, user_id: str, user: User) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        data = user.model_dump(by_alias=True, exclude={"id"})
        await doc_ref.set(data)
        user.id = user_id
        return user

    # ------------------------------------------------------------------ UPDATE ESPECÍFICOS

    async def set_tutoring(self, user_id: str, is_tutoring: bool) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"isTutoring": is_tutoring})
        return self._doc_to_user(await doc_ref.get())

    async def update_availability(self, user_id: str, availability: Availability) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"availability": availability.model_dump(by_alias=True)})
        return self._doc_to_user(await doc_ref.get())

    async def update_tutoring_skills(self, user_id: str, skill_ids: list[str]) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"tutoringSkills": skill_ids})
        return self._doc_to_user(await doc_ref.get())

    async def update_interested_skills(self, user_id: str, skill_ids: list[str]) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"interestedSkills": skill_ids})
        return self._doc_to_user(await doc_ref.get())

    async def update_fav_tutors(self, user_id: str, fav_tutor_ids: list[str]) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"favTutors": fav_tutor_ids})
        return self._doc_to_user(await doc_ref.get())

    # -------- Payment Methods

    async def add_payment_method(self, user_id: str, method: PaymentMethod) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        current: list = doc.to_dict().get("paymentMethods", [])
        if len(current) >= 3:
            raise ValueError("El usuario ya tiene 3 métodos de pago registrados.")
        await doc_ref.update({
            "paymentMethods": ArrayUnion([method.model_dump(by_alias=True)])
        })
        return self._doc_to_user(await doc_ref.get())

    async def remove_payment_method(self, user_id: str, card_number: str) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        current: list[dict] = doc.to_dict().get("paymentMethods", [])
        updated = [m for m in current if m.get("number") != card_number]
        await doc_ref.update({"paymentMethods": updated})
        return self._doc_to_user(await doc_ref.get())

    # -------- FCM Tokens

    async def add_fcm_token(self, user_id: str, token: str) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"fcmTokens": ArrayUnion([token])})
        return self._doc_to_user(await doc_ref.get())

    async def remove_fcm_token(self, user_id: str, token: str) -> User | None:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"fcmTokens": ArrayRemove([token])})
        return self._doc_to_user(await doc_ref.get())

    # ------------------------------------------------------------------ DELETE
    async def delete(self, user_id: str) -> bool:
        doc_ref = self.col.document(user_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        await doc_ref.delete()
        return True
    

    async def get_users_with_fav_tutor(self, tutor_id: str) -> list[User]:
        """Retorna todos los usuarios que tienen a tutor_id en su lista de favoritos."""
        docs = await (
            self.col
            .where("favTutors", "array-contains", tutor_id)
            .get()
        )
        return [self._doc_to_user(doc) for doc in docs]

