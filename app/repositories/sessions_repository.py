# app/repositories/session_repository.py
import random
import string
from datetime import datetime, timezone
from google.cloud.firestore_v1 import AsyncClient
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
        return Session(id=doc.id, **doc.to_dict())

    # ------------------------------------------------------------------ CREATE
    async def create(self, session: Session) -> Session:
        doc_ref = self.col.document()
        session.verif_code = _generate_verif_code()   # ← generado en servidor
        data = session.model_dump(by_alias=True, exclude={"id"})
        await doc_ref.set(data)
        session.id = doc_ref.id
        return session

    # ------------------------------------------------------------------ READ
    async def get_all(self) -> list[Session]:
        docs = await self.col.get()
        return [self._doc_to_session(doc) for doc in docs]
    
    async def get_by_id(self, session_id: str) -> Session | None:
        doc = await self.col.document(session_id).get()
        if not doc.exists:
            return None
        return self._doc_to_session(doc)

    async def get_by_student(self, student_id: str) -> list[Session]:
        docs = await (
            self.col
            .where("studentId", "==", student_id)
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]

    async def get_by_tutor(self, tutor_id: str) -> list[Session]:
        docs = await (
            self.col
            .where("tutorId", "==", tutor_id)
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]

    async def get_by_student_and_status(self, student_id: str, status: SessionStatus) -> list[Session]:
        docs = await (
            self.col
            .where("studentId", "==", student_id)
            .where("status", "==", status.value)
            .order_by("scheduledAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]

    async def get_by_tutor_and_status(self, tutor_id: str, status: SessionStatus) -> list[Session]:
        docs = await (
            self.col
            .where("tutorId", "==", tutor_id)
            .where("status", "==", status.value)
            .order_by("scheduledAt", direction="DESCENDING")
            .get()
        )
        return [self._doc_to_session(doc) for doc in docs]

    async def get_session_between(self, student_id: str, tutor_id: str) -> list[Session]:
        """Todas las sesiones entre un estudiante y un tutor específicos."""
        docs = await (
            self.col
            .where("studentId", "==", student_id)
            .where("tutorId", "==", tutor_id)
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
