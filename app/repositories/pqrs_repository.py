# app/repositories/pqr_repository.py

from datetime import datetime, timezone
from google.cloud.firestore_v1 import AsyncClient
from app.models.pqrs import PQR
from app.models.enums import SessionStatus, PQRType

COLLECTION = "pqrs"


class PQRRepository:

    def __init__(self, db: AsyncClient):
        self.db = db
        self.col = db.collection(COLLECTION)

    # ------------------------------------------------------------------ HELPERS
    def _doc_to_pqr(self, doc) -> PQR:
        return PQR(id=doc.id, **doc.to_dict())

    # ------------------------------------------------------------------ CREATE
    async def create(self, pqr: PQR) -> PQR:
        doc_ref = self.col.document()
        data = pqr.model_dump(by_alias=True, exclude={"id"})
        data["createdAt"] = datetime.now(timezone.utc)  # asignado en servidor
        await doc_ref.set(data)
        pqr.id = doc_ref.id
        pqr.created_at = data["createdAt"]
        return pqr

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, pqr_id: str) -> PQR | None:
        doc = await self.col.document(pqr_id).get()
        if not doc.exists:
            return None
        return self._doc_to_pqr(doc)

    async def get_by_author(self, author_id: str) -> list[PQR]:
        docs = await (
            self.col
            .where("authorId", "==", author_id)
            .order_by("createdAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_pqr(doc) for doc in docs]

    async def get_by_status(self, status: SessionStatus) -> list[PQR]:
        docs = await (
            self.col
            .where("status", "==", status.value)
            .order_by("createdAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_pqr(doc) for doc in docs]

    async def get_by_type(self, pqr_type: PQRType) -> list[PQR]:
        docs = await (
            self.col
            .where("type", "==", pqr_type.value)
            .order_by("createdAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_pqr(doc) for doc in docs]

    async def get_by_related_incident(self, session_id: str) -> list[PQR]:
        """Todos los PQRs asociados a una sesión específica."""
        docs = await (
            self.col
            .where("relatedIncident", "==", session_id)
            .get()
        )
        return [self._doc_to_pqr(doc) for doc in docs]

    # ------------------------------------------------------------------ UPDATE
    async def update_status(self, pqr_id: str, status: SessionStatus) -> PQR | None:
        doc_ref = self.col.document(pqr_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"status": status.value})
        return self._doc_to_pqr(await doc_ref.get())

    # ------------------------------------------------------------------ DELETE
    async def delete(self, pqr_id: str) -> bool:
        doc_ref = self.col.document(pqr_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        await doc_ref.delete()
        return True
