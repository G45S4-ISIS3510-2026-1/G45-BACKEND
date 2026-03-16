# app/mockData/sessions.py

from datetime import datetime, timezone

MOCK_SESSIONS: list[dict] = [
    {
        "_student_index": 2,   # Andrés
        "_tutor_index":   0,   # Nicolás
        "_skill_index":   0,   # Estructuras de Datos (primer skill)
        "scheduledAt": datetime(2026, 3, 23, 9, 0, 0, tzinfo=timezone.utc),
    },
    {
        "_student_index": 2,   # Andrés
        "_tutor_index":   1,   # Laura
        "_skill_index":   2,   # Cálculo Diferencial (tercer skill)
        "scheduledAt": datetime(2026, 3, 24, 10, 0, 0, tzinfo=timezone.utc),
    },
]
