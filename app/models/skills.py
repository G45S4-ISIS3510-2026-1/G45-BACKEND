# app/models/skill.py

from __future__ import annotations
from pydantic import BaseModel, Field
from app.models.enums import UniandesMajor


class Skill(BaseModel):
    """Documento de la colección 'skills' en Firestore."""

    id: str | None = Field(
        default=None,
        description="ID del documento en Firestore (se asigna tras la creación)"
    )
    major:    UniandesMajor = Field(..., description="Carrera a la que pertenece la habilidad")
    label:    str           = Field(..., description="Nombre de la materia o habilidad")
    icon_url: str           = Field(..., alias="iconUrl", description="URL del ícono o imagen representativa")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "major": "Ingeniería de Sistemas y Computación",
                "label": "Estructuras de Datos",
                "iconUrl": "https://cdn.example.com/icons/data-structures.png"
            }
        }
    }
