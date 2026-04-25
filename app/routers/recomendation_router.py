from fastapi import APIRouter, Depends, Query
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

@router.post("/recommendations", response_model=list[TutorSummary])
async def suggest_tutors(searched_ids: list[str], svc: RecommenderService = RS, n_top: int | None = Query(default=5, ge=1, le=20, description="Número de recomendaciones a retornar")):
    recommendations = await svc.get_recommendations(searched_ids, n_top=n_top)
    tutor_summaries = []
    for tutor in recommendations:
        tutor_summaries.append(
            TutorSummary(
                id=tutor.id,
                name=tutor.name,
                major=tutor.major,
                tutor_rating=tutor.tutorRating,
                received_ratings=tutor.receivedRatings,
                profile_image_url=tutor.profile_image_url,
                session_price=tutor.session_price,
            )
        )
    return tutor_summaries