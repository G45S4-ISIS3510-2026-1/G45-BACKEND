# app/models/review.py

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Review(BaseModel):
    """Documento de la colección 'reviews' en Firestore."""

    id: str | None = Field(
        default=None,
        description="ID del documento en Firestore (se asigna tras la creación)"
    )
    author_id: str = Field(..., alias="authorId", description="ID del usuario que escribe la review")
    tutor_id:  str = Field(..., alias="tutorId",  description="ID del tutor que recibe la review")
    rating:    float = Field(..., ge=0.0, le=5.0,  description="Calificación entre 0.0 y 5.0")
    label:     str = Field(..., max_length=50,      description="Título corto de la review")
    details:   str = Field(...,                     description="Descripción o detalles de la review")
    created_at: datetime|None = Field(default=None, alias="createdAt", description="Fecha y hora de publicación")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "authorId":  "uid_estudiante_1",
                "tutorId":   "uid_tutor_1",
                "rating":    4.5,
                "label":     "Excelente explicación de Cálculo",
                "details":   "El tutor fue muy claro y paciente. Resolvió todas mis dudas.",
                "createdAt": "2026-03-15T16:00:00"
            }
        }
    }

    @field_validator("rating")
    @classmethod
    def round_rating(cls, v: float) -> float:
        """Redondea el rating a un decimal para consistencia (ej: 4.55 → 4.6)."""
        return round(v, 1)
