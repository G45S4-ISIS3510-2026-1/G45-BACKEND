# app/models/user.py

from __future__ import annotations
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator

# app/models/user.py  — sección de imports

from app.models.enums import UniandesMajor
from app.models.skills import Skill

# ---------------------------------------------------------------------------
# Sub-modelos
# ---------------------------------------------------------------------------

class PaymentMethod(BaseModel):
    """Tarjeta de crédito asociada al usuario (máximo 3)."""
    number:    str = Field(..., description="Número de la tarjeta")
    cvv:       str = Field(..., min_length=3, max_length=4, description="Código CVV")
    holder:    str = Field(..., description="Nombre del titular")
    exp_month: int = Field(..., ge=1, le=12, description="Mes de vencimiento")
    exp_year:  int = Field(..., ge=2024, description="Año de vencimiento")


class Availability(BaseModel):
    """Franjas horarias disponibles por día (timestamps)."""
    monday:    list[datetime] = Field(default_factory=list)
    tuesday:   list[datetime] = Field(default_factory=list)
    wednesday: list[datetime] = Field(default_factory=list)
    thursday:  list[datetime] = Field(default_factory=list)
    friday:    list[datetime] = Field(default_factory=list)
    saturday:  list[datetime] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Modelo principal
# ---------------------------------------------------------------------------

# app/models/user.py  — cambios relevantes (resto del archivo igual)



class User(BaseModel):
    """Documento de la colección 'users' en Firestore."""

    id: str | None = Field(default=None)
    name:  str      = Field(..., description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico")
    major: UniandesMajor = Field(..., description="Carrera de pregrado del usuario")
    is_tutoring: bool = Field(default=False, alias="isTutoring")
    uniandes_id: int  = Field(..., alias="uniandesId")
    fcm_tokens:  list[str] = Field(default_factory=list, alias="fcmTokens")
    fav_tutors:  list[str] = Field(default_factory=list, alias="favTutors")

    tutoring_skills: list[str] = Field(          # ← solo IDs
        default_factory=list,
        alias="tutoringSkills",
        description="IDs de skills que el usuario puede tutoriar"
    )
    interested_skills: list[str] = Field(        # ← solo IDs
        default_factory=list,
        alias="interestedSkills",
        description="IDs de skills en los que el usuario busca tutoría"
    )

    availability: Availability = Field(default_factory=Availability)
    payment_methods: Annotated[
        list[PaymentMethod],
        Field(max_length=3)
    ] = Field(default_factory=list, alias="paymentMethods")
    
    session_price: int = Field(
        default=0,
        alias="sessionPrice",
        ge=0,
        description="Precio por sesión en pesos colombianos (solo aplica si isTutoring=True)"
    )
    
    # app/models/user.py — agrega el campo

    profile_image_url: str | None = Field(
        default=None,
        alias="profileImageUrl",
        description="URL de la imagen de perfil del usuario (puede actualizarse libremente)"
    )


    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "uid_user_1",
                "name": "Nicolás Ballén",
                "email": "n.ballen@uniandes.edu.co",
                "major": "Ingeniería de Sistemas y Computación",
                "isTutoring": True,
                "uniandesId": 202012345,
                "fcmTokens": ["token_abc123"],
                "favTutors": ["uid_tutor_1"],
                "tutoringSkills":  ["skill_001", "skill_002"],
                "interestedSkills": ["skill_042"],
                "availability": {
                    "monday": ["2026-03-16T09:00:00"],
                    "tuesday": [],
                    "wednesday": ["2026-03-18T14:00:00"],
                    "thursday": [],
                    "friday": [],
                    "saturday": []
                },
                "paymentMethods": [
                    {
                        "number": "4111111111111111",
                        "cvv": "123",
                        "holder": "Nicolás Ballén",
                        "exp_month": 12,
                        "exp_year": 2028
                    }
                ],
                "sessionPrice": 50000,
                "profileImageUrl": "https://example.com/profiles/nicolas.jpg"
            }
        }
    }

    @field_validator("payment_methods")
    @classmethod
    def max_three_payment_methods(cls, v: list[PaymentMethod]) -> list[PaymentMethod]:
        if len(v) > 3:
            raise ValueError("Un usuario no puede tener más de 3 métodos de pago.")
        return v
