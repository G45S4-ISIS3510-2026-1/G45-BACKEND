# app/services/review_service.py

from fastapi import HTTPException, status
from app.dtos.review_response import ReviewResponse
from app.models.reviews import Review
from app.repositories.reviews_repository import ReviewRepository
from app.repositories.user_repository import UserRepository


class ReviewService:

    def __init__(self, review_repo: ReviewRepository, user_repo: UserRepository):
        self.review_repo = review_repo
        self.user_repo   = user_repo

    # ------------------------------------------------------------------ CREATE
    async def create(self, review: Review) -> Review:
        # Validar existencia del autor
        author = await self.user_repo.get_by_id(review.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El autor '{review.author_id}' no existe."
            )
        # Validar existencia del tutor y que efectivamente sea tutor
        tutor = await self.user_repo.get_by_id(review.tutor_id)
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El tutor '{review.tutor_id}' no existe."
            )
        if not tutor.is_tutoring:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario '{review.tutor_id}' no es tutor."
            )
        # Un autor no puede reseñarse a sí mismo
        if review.author_id == review.tutor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un usuario no puede reseñarse a sí mismo."
            )
        # Un autor solo puede dejar una review por tutor
        existing = await self.review_repo.get_by_tutor_and_author(
            review.tutor_id, review.author_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El usuario '{review.author_id}' ya dejó una reseña al tutor '{review.tutor_id}'."
            )
        tutor.tutorRating=tutor.tutorRating+review.rating/(tutor.receivedRatings+1)
        tutor.receivedRatings=tutor.receivedRatings+1
        await self.user_repo.update(tutor.id, tutor)
        return await self.review_repo.create(review)

    # ------------------------------------------------------------------ READ
    async def get_by_id(self, review_id: str) -> Review:
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review '{review_id}' no encontrada."
            )
        return review
    #Cambio para Carga review
    async def get_by_tutor(self, tutor_id: str) -> list[ReviewResponse]:
        reviews = await self.review_repo.get_by_tutor(tutor_id)

        enriched_reviews = []

        for review in reviews:
            user = await self.user_repo.get_by_id(review.author_id)

            enriched_reviews.append(ReviewResponse(
                authorId=review.author_id,
                authorName=user.name,
                authorImage=user.profile_image_url,
                label=review.label,
                details=review.details,
                rating=review.rating,
                createdAt=review.created_at,
            ))

        return enriched_reviews

    async def get_by_author(self, author_id: str) -> list[Review]:
        if not await self.user_repo.get_by_id(author_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario '{author_id}' no encontrado."
            )
        return await self.review_repo.get_by_author(author_id)


    # ------------------------------------------------------------------ DELETE
    async def delete(self, review_id: str, requesting_user_id: str) -> bool:
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review '{review_id}' no encontrada."
            )
        # Solo el autor puede eliminar su propia review
        if review.author_id != requesting_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el autor puede eliminar su propia reseña."
            )
        tutor=await self.user_repo.get_by_id(review.tutor_id)
        tutor.tutorRating=(tutor.tutorRating*tutor.receivedRatings-review.rating)/(tutor.receivedRatings-1)
        tutor.receivedRatings=tutor.receivedRatings-1
        await self.user_repo.update(tutor.id, tutor)

        return await self.review_repo.delete(review_id)
