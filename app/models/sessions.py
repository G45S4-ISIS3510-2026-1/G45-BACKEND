# app/models/session.py

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import SessionStatus
from app.models.skills import Skill


class Session(BaseModel):
    """Documento de la colección 'sessions' en Firestore."""

    id: str | None = Field(
        default=None,
        description="ID del documento en Firestore (se asigna tras la creación)"
    )
    student_id:   str           = Field(..., alias="studentId",   description="ID del usuario estudiante")
    tutor_id:     str           = Field(..., alias="tutorId",     description="ID del usuario tutor")
    scheduled_at: datetime      = Field(..., alias="scheduledAt", description="Fecha y hora en que ocurrirá la sesión")
    status:       SessionStatus = Field(default=SessionStatus.PENDIENTE, description="Estado actual de la sesión")
    verif_code:   str  | None         = Field(default=None, alias="verifCode",   description="Código alfanumérico de verificación de la sesión")
    skill: Skill = Field(..., description="Skill principal de la tutoría (instancia completa)")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "studentId":   "uid_estudiante_1",
                "tutorId":     "uid_tutor_1",
                "scheduledAt": "2026-03-20T10:00:00",
                "status":      "Pendiente",
                "verifCode":   "A3X9KQ",
                "skill": {
                    "id": "skill_001",
                    "major": "Programación en Python",
                    "label": "Habilidad para programar en lenguaje Python",
                    "icon_url": "https://cdn.example.com/icons/python.png"
                }

            }
        }
    }
