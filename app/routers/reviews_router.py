# app/routers/review_router.py

from fastapi import APIRouter, Depends
from app.models.reviews import Review
from app.services.reviews_service import ReviewService
from app.dtos.review_response import ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# ------------------------------------------------------------------ Dependencias

from app.dependencies import (
    get_review_service
)

RS = Depends(get_review_service)


# ------------------------------------------------------------------ CREATE

@router.post("/", response_model=Review, status_code=201)
async def create_review(review: Review, svc: ReviewService = RS):
    return await svc.create(review)


# ------------------------------------------------------------------ READ

@router.get("/{review_id}", response_model=Review)
async def get_by_id(review_id: str, svc: ReviewService = RS):
    return await svc.get_by_id(review_id)

@router.get("/by-tutor/{tutor_id}", response_model=list[ReviewResponse])
async def get_by_tutor(tutor_id: str, svc: ReviewService = RS):
    return await svc.get_by_tutor(tutor_id)

@router.get("/by-author/{author_id}", response_model=list[Review])
async def get_by_author(author_id: str, svc: ReviewService = RS):
    return await svc.get_by_author(author_id)

# ------------------------------------------------------------------ DELETE

@router.delete("/{review_id}/by/{requesting_user_id}", status_code=204)
async def delete_review(review_id: str, requesting_user_id: str, svc: ReviewService = RS):
    await svc.delete(review_id, requesting_user_id)
