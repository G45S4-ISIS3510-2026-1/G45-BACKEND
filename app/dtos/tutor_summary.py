from pydantic import BaseModel, Field
from app.models.enums import UniandesMajor

class TutorSummary(BaseModel):
    id: str
    name: str
    major: UniandesMajor
    profile_image_url: str | None = None
    session_price: int | None = None
    tutor_rating: float = Field(default=0.0, alias="tutorRating")
    received_ratings: int = Field(default=0, alias="receivedRatings")

    model_config = {"populate_by_name": True}