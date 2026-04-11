# app/mockData/pqrs.py

from app.models.enums import PQRType

MOCK_PQRS: list[dict] = [
    # --- Quejas vinculadas a sesiones ---
    {
        "_author_index":   10,  # Andrés
        "_session_index":  0,   # Sesión con Nicolás
        "type":            PQRType.QUEJA,
        "topic":           "Tutor llegó tarde",
        "description":     "El tutor se conectó 15 minutos después de la hora acordada.",
    },
    {
        "_author_index":   11,  # Camila
        "_session_index":  1,   # Sesión con Laura
        "type":            PQRType.RECLAMO,
        "topic":           "Problemas de conexión",
        "description":     "La plataforma se cayó a mitad de la sesión de Cálculo y no pudimos terminar.",
    },
    {
        "_author_index":   12,  # Jorge
        "_session_index":  2,   # Sesión con Carlos
        "type":            PQRType.QUEJA,
        "topic":           "Ambiente ruidoso",
        "description":     "Había mucho ruido de fondo por parte del tutor, lo que dificultó la explicación.",
    },

    # --- Peticiones y Sugerencias generales (sin sesión) ---
    {
        "_author_index":   10,  # Andrés
        "_session_index":  None,
        "type":            PQRType.PETICION,
        "topic":           "Solicitud de nuevas materias",
        "description":     "Me gustaría que hubiera tutores para materias de posgrado en IA.",
    },
    {
        "_author_index":   13,  # Mariana
        "_session_index":  None,
        "type":            PQRType.PETICION,
        "topic":           "Métodos de pago",
        "description":     "Sería excelente poder pagar sesiones directamente con Nequi o Daviplata.",
    },
    {
        "_author_index":   14,  # Sebastian
        "_session_index":  None,
        "type":            PQRType.PETICION,
        "topic":           "Interfaz de usuario",
        "description":     "Solicito un modo oscuro para la aplicación móvil, me cansa mucho la vista.",
    },

    # --- Casos adicionales mixtos ---
    {
        "_author_index":   11,  # Camila
        "_session_index":  6,   # Sesión con Valentina
        "type":            PQRType.RECLAMO,
        "topic":           "Cobro incorrecto",
        "description":     "Se me realizó un doble cobro en la tarjeta al agendar la monitoría de Psicología.",
    },
    {
        "_author_index":   12,  # Jorge
        "_session_index":  7,   # Sesión con Felipe
        "type":            PQRType.PETICION,
        "topic":           "Grabación de sesiones",
        "description":     "¿Es posible que implementen una opción para grabar la pantalla durante la tutoría?",
    },
    {
        "_author_index":   13,  # Mariana
        "_session_index":  None,
        "type":            PQRType.PETICION,
        "topic":           "Certificados",
        "description":     "Quisiera saber si la plataforma emite certificados de horas de monitoría recibidas.",
    },
    {
        "_author_index":   14,  # Sebastian
        "_session_index":  9,   # Sesión con Mateo
        "type":            PQRType.QUEJA,
        "topic":           "Material no compartido",
        "description":     "El tutor quedó de enviarme un PDF con ejercicios y aún no lo recibo.",
    },
]