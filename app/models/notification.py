

from pydantic import BaseModel, Field


class NotificationPayload(BaseModel):
    """Datos necesarios para construir y enviar una notificación push."""
    title: str = Field(..., description="Título de la notificación")
    body:  str = Field(..., description="Cuerpo o mensaje de la notificación")
    data:  dict[str, str] | None = Field(
        default=None,
        description="Payload de datos adicionales (clave-valor strings) para la app"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Nueva sesión reservada",
                "body":  "Tienes una tutoría de Cálculo el lunes a las 9:00 AM.",
                "data":  {
                    "sessionId": "session_abc123",
                    "type":      "SESSION_BOOKED"
                }
            }
        }
    }
