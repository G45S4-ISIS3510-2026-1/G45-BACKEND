# app/repositories/skill_repository.py

from google.cloud.firestore_v1 import AsyncClient
from app.models.skills import Skill

COLLECTION = "skills"


class SkillRepository:

    def __init__(self, db: AsyncClient):
        self.db = db
        self.col = db.collection(COLLECTION)

    # ------------------------------------------------------------------ CREATE
    async def create(self, skill: Skill) -> Skill:
        doc_ref = self.col.document()
        data = skill.model_dump(by_alias=True, exclude={"id"})
        await doc_ref.set(data)
        skill.id = doc_ref.id
        return skill

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, skill_id: str) -> Skill | None:
        doc = await self.col.document(skill_id).get()
        if not doc.exists:
            return None
        return Skill(id=doc.id, **doc.to_dict())

    async def get_all(self) -> list[Skill]:
        docs = await self.col.get()
        return [Skill(id=doc.id, **doc.to_dict()) for doc in docs]

    async def get_by_major(self, major: str) -> list[Skill]:
        docs = await self.col.where("major", "==", major).get()
        return [Skill(id=doc.id, **doc.to_dict()) for doc in docs]

    # ------------------------------------------------------------------ UPDATE
    async def update_icon_url(self, skill_id: str, icon_url: str) -> Skill | None:
        doc_ref = self.col.document(skill_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        await doc_ref.update({"iconUrl": icon_url})
        return Skill(id=doc.id, **{**doc.to_dict(), "iconUrl": icon_url})

    # ------------------------------------------------------------------ DELETE
    async def delete(self, skill_id: str) -> bool:
        doc_ref = self.col.document(skill_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        await doc_ref.delete()
        return True
