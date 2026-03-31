# app/models/pqr.py

from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import SessionStatus, PQRType


class PQR(BaseModel):
    """Documento de la colección 'pqrs' en Firestore."""

    id: str | None = Field(
        default=None,
        description="ID del documento en Firestore (se asigna tras la creación)"
    )
    type:        PQRType       = Field(..., alias="type",        description="Tipo de PQR")
    status:      SessionStatus = Field(default=SessionStatus.PENDIENTE, description="Estado del PQR")
    topic:       str           = Field(...,                      description="Asunto del PQR")
    description: str           = Field(...,                      description="Detalle de la situación")
    author_id:   str           = Field(..., alias="authorId",    description="ID del usuario que genera el PQR")
    created_at:  datetime|None      = Field(default=None, alias="createdAt",   description="Fecha y hora de creación")
    related_incident: str | None = Field(
        default=None,
        alias="relatedIncident",
        description="ID de la sesión relacionada (opcional)"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "type":             "Queja",
                "status":           "Pendiente",
                "topic":            "Tutor no se presentó a la sesión",
                "description":      "El tutor confirmó la sesión pero nunca se conectó a la videollamada.",
                "authorId":         "uid_estudiante_1",
                "createdAt":        "2026-03-15T16:30:00",
                "relatedIncident":  "session_id_abc123"
            }
        }
    }
