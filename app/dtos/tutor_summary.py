from pydantic import BaseModel
from app.models.enums import UniandesMajor

class TutorSummary(BaseModel):
    id: str
    name: str
    major: UniandesMajor
    rating: float | None = None
    profile_image_url: str | None = None
    session_price: int | None = None