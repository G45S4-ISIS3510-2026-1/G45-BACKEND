# app/repositories/session_repository.py
import random
import string
from datetime import datetime, timezone
from google.cloud.firestore_v1 import AsyncClient, FieldFilter
from app.core.currentWeekManager import getColombiaTimezone, refactorTimezone
from app.models.sessions import Session
from app.models.enums import SessionStatus

COLLECTION = "sessions"

def _generate_verif_code(length: int = 6) -> str:
    """Genera un código alfanumérico aleatorio en mayúsculas."""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


class SessionRepository:

    def __init__(self, db: AsyncClient):
        self.db = db
        self.col = db.collection(COLLECTION)

    # ------------------------------------------------------------------ HELPERS
    def _doc_to_session(self, doc) -> Session:
        session= Session(id=doc.id, **doc.to_dict())
        #presentar scheduled_at en timezone de Colombia para evitar confusiones (Firestore siempre guarda en UTC)
        session.scheduled_at = refactorTimezone(session.scheduled_at)
        return session

    # ------------------------------------------------------------------ CREATE
    async def create(self, session: Session) -> Session:
        doc_ref = self.col.document()
        session.verif_code = _generate_verif_code()   # ← generado en servidor
        data = session.model_dump(by_alias=True, exclude={"id"})
        #corregir timezone a UTC para evitar problemas con Firestore (que siempre guarda en UTC)
        timezoneColombia = getColombiaTimezone()
        if session.scheduled_at.tzinfo is None or session.scheduled_at.tzinfo != timezoneColombia :
            correction= session.scheduled_at.replace(tzinfo=None)
            data["scheduledAt"] = correction.replace(tzinfo=getColombiaTimezone())
        await doc_ref.set(data)
        session.id = doc_ref.id
        return session

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, session_id: str) -> Session | None:
        doc = await self.col.document(session_id).get()
        if not doc.exists:
            return None
        return self._doc_to_session(doc)

    async def get_by_student(self, student_id: str) -> list[Session]:
        print(f"Buscando sesiones para studentId={student_id}...")
        
        docs = await (
            self.col
            .where(filter=FieldFilter("student.id", "==", student_id))
            .order_by("scheduledAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]

    async def get_by_tutor(self, tutor_id: str) -> list[Session]:
        docs = await (
            self.col
            .where(filter=FieldFilter("tutor.id", "==", tutor_id))
            .order_by("scheduledAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]

    async def get_by_tutor_and_student(self, tutor_id: str, student_id: str) -> list[Session]:
        docs = await (
            self.col
            .where(filter=FieldFilter("tutor.id", "==", tutor_id))
            .where(filter=FieldFilter("student.id", "==", student_id))
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]
    # ------------------------------------------------------------------ UPDATE
    async def update_status(self, session_id: str, status: SessionStatus) -> Session | None:
        doc_ref = self.col.document(session_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"status": status.value})
        return self._doc_to_session(await doc_ref.get())

    # ------------------------------------------------------------------ DELETE
    async def delete(self, session_id: str) -> bool:
        doc_ref = self.col.document(session_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        await doc_ref.delete()
        return True
