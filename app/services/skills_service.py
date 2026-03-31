# app/services/skill_service.py

from fastapi import HTTPException, status
from app.models.skills import Skill
from app.models.enums import UniandesMajor
from app.repositories.skills_repository import SkillRepository


class SkillService:

    def __init__(self, repo: SkillRepository):
        self.repo = repo

    # ------------------------------------------------------------------ CREATE
    async def create(self, skill: Skill) -> Skill:
        # Evitar skills duplicados: mismo label en la misma carrera
        existing = await self.repo.get_by_major(skill.major.value)
        conflict = any(
            s.label.strip().lower() == skill.label.strip().lower()
            for s in existing
        )
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un skill '{skill.label}' para la carrera '{skill.major.value}'."
            )
        return await self.repo.create(skill)

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, skill_id: str) -> Skill:
        skill = await self.repo.get_by_id(skill_id)
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill '{skill_id}' no encontrado."
            )
        return skill

    async def get_all(self) -> list[Skill]:
        return await self.repo.get_all()

    async def get_by_major(self, major: UniandesMajor) -> list[Skill]:
        return await self.repo.get_by_major(major.value)

    # ------------------------------------------------------------------ UPDATE
    async def update_icon_url(self, skill_id: str, icon_url: str) -> Skill:
        if not icon_url.startswith(("http://", "https://")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El icon_url debe ser una URL válida (http/https)."
            )
        skill = await self.repo.update_icon_url(skill_id, icon_url)
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Skill '{skill_id}' no encontrado."
            )
        return skill
    

    async def get_all_majors(self) -> list[str]:
        """Retorna todos los valores válidos de carreras de pregrado."""
        return [major.value for major in UniandesMajor]

