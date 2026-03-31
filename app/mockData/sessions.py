# app/mockData/sessions.py

from datetime import datetime, timezone

from app.core.currentWeekManager import getColombiaTimezone

MOCK_SESSIONS: list[dict] = [
    {  # Andrés
        "student": {
            "id": 2,
            "name": "Andrés Gomez"
        },
        "tutor":{
            "id": 0,
            "name": "Nicolás Ballen"
        },
        "skill":   {
            "id": 0,
            "label": "Estructuras de Datos"
        },
        "scheduledAt": datetime(2026, 3, 23, 9, 0, 0, tzinfo=getColombiaTimezone()),
    },
    {
        "student": {
            "id": 2,
            "name": "Andrés Gomez"
        },
        "tutor":{
            "id": 1,
            "name": "Laura Martínez"
        },
        "skill":   {
            "id": 2,
            "label": "Cálculo Diferencial"
        },
        "scheduledAt": datetime(2026, 3, 24, 10, 0, 0, tzinfo=getColombiaTimezone()),
    },
]
