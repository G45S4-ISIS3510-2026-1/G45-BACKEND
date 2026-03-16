# app/mockData/pqrs.py

from app.models.enums import PQRType

MOCK_PQRS: list[dict] = [
    {
        "_author_index":   2,    # Andrés
        "_session_index":  0,    # sesión Andrés → Nicolás
        "type":            PQRType.QUEJA,
        "topic":           "Tutor llegó tarde",
        "description":     "El tutor se conectó 15 minutos después de la hora acordada.",
    },
    {
        "_author_index":   2,    # Andrés
        "_session_index":  None, # sin sesión relacionada
        "type":            PQRType.PETICION,
        "topic":           "Solicitud de nuevas materias",
        "description":     "Me gustaría que hubiera tutores de Física Cuántica.",
    },
]
