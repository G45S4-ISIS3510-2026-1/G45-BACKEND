# app/models/session.py

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import SessionStatus
from app.models.skills import Skill

class ParticipantSummary(BaseModel):
    """Resumen básico de un participante en la sesión (tutor o estudiante)."""
    id: str = Field(..., description="ID del usuario")
    name: str = Field(..., description="Nombre completo del usuario")
    profileImageUrl: str | None = Field(default=None, alias="profileImageUrl", description="URL de la imagen de perfil del usuario")
    
class SkillSummary(BaseModel):
    """Resumen de la habilidad principal de la sesión."""
    id: str = Field(..., description="ID de la habilidad")
    label: str = Field(..., description="Nombre de la habilidad")

class Session(BaseModel):
    """Documento de la colección 'sessions' en Firestore."""

    id: str | None = Field(
        default=None,
        description="ID del documento en Firestore (se asigna tras la creación)"
    )
    price: int = Field(
        default=0, alias="price",
        ge=0, description="Precio de la sesión en pesos colombianos (debe ser igual al sessionPrice del tutor al momento de crear la sesión)"
    )
    scheduled_at: datetime      = Field(..., alias="scheduledAt", description="Fecha y hora en que ocurrirá la sesión")
    status:       SessionStatus = Field(default=SessionStatus.PENDIENTE, description="Estado actual de la sesión")
    verif_code:   str  |None         = Field(default=None, alias="verifCode",   description="Código alfanumérico de verificación de la sesión")
    skill: SkillSummary|None = Field(default=None, description="Resumen de la habilidad principal de la tutoría")
    student: ParticipantSummary = Field(..., description="Resumen del estudiante participante")
    tutor: ParticipantSummary = Field(..., description="Resumen del tutor participante")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "student": {
                    "id": "uid_estudiante_123",
                    "name": "Ana Gómez",
                    "profileImageUrl": "https://example.com/images/ana.jpg"
                },
                "tutor": {
                    "id": "uid_tutor_123",
                    "name": "Carlos Rodríguez",
                    "profileImageUrl": "https://example.com/images/carlos.jpg"
                },
                "scheduledAt": "2026-03-20T10:00:00",
                "status":      "Pendiente",
                "price":       15000,
                "verifCode":   "A3X9KQ",
                "skill": {
                    "id": "skill_001",
                    "label": "Habilidad para programar en lenguaje Python"
                }

            }
        }
    }
