# app/routers/skill_router.py

from fastapi import APIRouter, Query, Depends
from app.models.skills import Skill
from app.models.enums import UniandesMajor
from app.services.skills_service import SkillService

router = APIRouter(prefix="/skills", tags=["Skills"])


# ------------------------------------------------------------------ Dependencias

from app.dependencies import (
    get_skill_service
)

SS = Depends(get_skill_service)


# ------------------------------------------------------------------ CREATE

@router.post("/", response_model=Skill, status_code=201)
async def create_skill(skill: Skill, svc: SkillService = SS):
    return await svc.create(skill)


# ------------------------------------------------------------------ READ

@router.get("/majors", response_model=list[str])
async def get_all_majors(svc: SkillService = SS):
    return await svc.get_all_majors()

@router.get("/", response_model=list[Skill])
async def get_all(svc: SkillService = SS):
    return await svc.get_all()

@router.get("/by-major/{major}", response_model=list[Skill])
async def get_by_major(major: UniandesMajor, svc: SkillService = SS):
    return await svc.get_by_major(major)

@router.get("/by-ids", response_model=list[Skill])
async def get_by_ids(
    ids: list[str] = Query(..., description="Lista de IDs de skills a consultar"),
    svc: SkillService = SS,
):
    skills = []
    for skill_id in ids:
        skills.append(await svc.get_by_id(skill_id))
    return skills


# ------------------------------------------------------------------ UPDATE

@router.patch("/{skill_id}/icon", response_model=Skill)
async def update_icon_url(
    skill_id: str,
    icon_url: str = Query(..., description="Nueva URL del ícono del skill"),
    svc:      SkillService = SS,
):
    return await svc.update_icon_url(skill_id, icon_url)


# ------------------------------------------------------------------ DELETE

#