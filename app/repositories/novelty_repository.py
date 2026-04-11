# app/repositories/novelties_repository.py

from datetime import datetime

from google.cloud.firestore_v1 import AsyncClient
from app.core.currentWeekManager import getColombiaTimezone
from app.models.novelty import Novelty

class NoveltiesRepository:
    def __init__(self, db: AsyncClient):
        self.db = db
        self.collection = self.db.collection("novelties")

    async def create_novelty(self, novelty: Novelty) -> str:
        """Crea una nueva novedad en Firestore."""
        novelty.created_at = novelty.created_at or datetime.now(getColombiaTimezone())
        doc_ref = self.collection.document()
        # Convertimos a dict usando alias para Firestore
        await doc_ref.set(novelty.model_dump(by_alias=True, exclude={"id"}))
        return doc_ref.id

    async def get_user_novelties(self, user_id: str, only_unread: bool = False) -> list[Novelty]:
        """Obtiene las novedades de un usuario específico."""
        query = self.collection.where("userId", "==", user_id)
        
        if only_unread:
            query = query.where("isRead", "==", False)
        
        # Ordenar por fecha de creación (requiere índice en Firestore)
        query = query.order_by("createdAt", direction="DESCENDING")
        
        docs = await query.get()
        return [Novelty(id=doc.id, **doc.to_dict()) for doc in docs]

    async def mark_as_read(self, novelty_id: str):
        """Marca una novedad como leída."""
        await self.collection.document(novelty_id).update({"isRead": True})