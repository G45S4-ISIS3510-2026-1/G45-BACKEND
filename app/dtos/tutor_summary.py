from pydantic import BaseModel, Field
from app.models.enums import UniandesMajor

class TutorSummary(BaseModel):
    id: str
    name: str
    major: UniandesMajor
    profile_image_url: str | None = None
    session_price: int | None = None
    tutoring_skills: list[str] = Field(default_factory=list, alias="tutoringSkills")
    tutor_rating: float = Field(default=0.0, alias="tutorRating")
    received_ratings: int = Field(default=0, alias="receivedRatings")
    sessions_completed: int = Field(default=0, alias="sessionsCompleted")

    model_config = {"populate_by_name": True}
