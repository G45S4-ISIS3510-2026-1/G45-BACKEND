from fastapi import APIRouter, Depends
from app.dtos.tutor_summary import TutorSummary
from app.models.user import User
from app.services.recommendation_service import RecommenderService
from app.services.recommendation_service import RecommenderService

router = APIRouter()
# ------------------------------------------------------------------ Dependencias

from app.dependencies import (
    get_recommender_service
)

RS = Depends(get_recommender_service)

@router.get("/recommendations", response_model=list[TutorSummary])
async def suggest_tutors(searched_ids: list[str], svc: RecommenderService = RS):
    await svc.load_all_tutors()
    recommendations = await svc.get_recommendations(searched_ids)
    tutor_summaries = []
    for tutor in recommendations:
        tutor_summaries.append(
            TutorSummary(
                id=tutor.id,
                name=tutor.name,
                major=tutor.major,
                rating=tutor.tutorRating,
                profile_image_url=tutor.profile_image_url,
                session_price=tutor.session_price,  
            )
        )
    return tutor_summaries