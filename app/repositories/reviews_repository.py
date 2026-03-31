# app/repositories/review_repository.py

from datetime import datetime, timezone
from google.cloud.firestore_v1 import AsyncClient
from app.core.currentWeekManager import getColombiaTimezone, refactorTimezone
from app.models.reviews import Review

COLLECTION = "reviews"


class ReviewRepository:

    def __init__(self, db: AsyncClient):
        self.db = db
        self.col = db.collection(COLLECTION)

    # ------------------------------------------------------------------ HELPERS
    def _doc_to_review(self, doc) -> Review:
        review= Review(id=doc.id, **doc.to_dict())
        #presentar created_at en timezone de Colombia para evitar confusiones (Firestore siempre guarda en UTC)
        review.created_at = refactorTimezone(review.created_at)
        return review

    # ------------------------------------------------------------------ CREATE
    async def create(self, review: Review) -> Review:
        doc_ref = self.col.document()
        data = review.model_dump(by_alias=True, exclude={"id"})
        data["createdAt"] = datetime.now(getColombiaTimezone())  # ← timestamp generado en servidor
        await doc_ref.set(data)
        review.id = doc_ref.id
        review.created_at = data["createdAt"]
        return review

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, review_id: str) -> Review | None:
        doc = await self.col.document(review_id).get()
        if not doc.exists:
            return None
        return self._doc_to_review(doc)

    async def get_by_tutor(self, tutor_id: str) -> list[Review]:
        """Todas las reviews recibidas por un tutor, de más reciente a más antigua."""
        docs = await (
            self.col
            .where("tutorId", "==", tutor_id)
            .order_by("createdAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_review(doc) for doc in docs]

    async def get_by_author(self, author_id: str) -> list[Review]:
        """Todas las reviews escritas por un usuario, de más reciente a más antigua."""
        docs = await (
            self.col
            .where("authorId", "==", author_id)
            .order_by("createdAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_review(doc) for doc in docs]

    async def get_by_tutor_and_author(self, tutor_id: str, author_id: str) -> Review | None:
        """Verifica si un autor ya dejó una review a un tutor específico."""
        docs = await (
            self.col
            .where("tutorId", "==", tutor_id)
            .where("authorId", "==", author_id)
            .limit(1)
            .get()
        )
        if not docs:
            return None
        return self._doc_to_review(docs[0])

    # ------------------------------------------------------------------ DELETE
    async def delete(self, review_id: str) -> bool:
        doc_ref = self.col.document(review_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        await doc_ref.delete()
        return True
