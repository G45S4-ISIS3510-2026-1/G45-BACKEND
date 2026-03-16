# app/mockData/sessions.py

from datetime import datetime, timezone

MOCK_SESSIONS: list[dict] = [
    {
        "_student_index": 2,  # Andrés
        "_tutor_index":   0,  # Nicolás
        # Lunes próximo a las 09:00 — dentro de la disponibilidad de Nicolás
        "scheduledAt": datetime(2026, 3, 23, 9, 0, 0, tzinfo=timezone.utc),
    },
    {
        "_student_index": 2,  # Andrés
        "_tutor_index":   1,  # Laura
        # Martes próximo a las 10:00 — dentro de la disponibilidad de Laura
        "scheduledAt": datetime(2026, 3, 24, 10, 0, 0, tzinfo=timezone.utc),
    },
]
