# app/models/novelty.py

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import NoveltyType

class Novelty(BaseModel):
    """Documento de la colección 'novelties' en Firestore."""
    
    id: str | None = Field(default=None)
    user_id: str = Field(..., alias="userId", description="ID del usuario destinatario")
    title: str = Field(..., description="Título de la notificación")
    description: str = Field(..., description="Descripción breve de la novedad")
    type: NoveltyType = Field(..., description="Tipo: PRECIO_CAMBIADO, SESION_RESERVADA, etc.")
    is_read: bool = Field(default=False, alias="isRead", description="Indica si el usuario ya vio la novedad")
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    entity_id: str | None = Field(default=None, alias="entityId", description="ID de la entidad relacionada (ej. sesión, tutoría)")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "userId": "uid_nicolas_123",
                "title": "¡Nueva sesión agendada!",
                "description": "Andrés Gómez ha reservado una tutoría contigo.",
                "type": "session_reserved",
                "isRead": False,
                "createdAt": "2026-04-11T17:25:00",
                "entityId": "session_456"
            }
        }
    }