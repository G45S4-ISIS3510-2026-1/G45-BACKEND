from pydantic import BaseModel
from datetime import datetime

class ReviewResponse(BaseModel):
    authorId: str
    authorName: str
    authorImage: str | None
    label: str
    details: str
    rating: float
    createdAt: datetime