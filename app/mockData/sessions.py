# app/mockData/sessions.py

from datetime import datetime, timedelta, timezone

# Configuración de zona horaria para Bogotá (UTC-5)
bog_tz = timezone(timedelta(hours=-5))

MOCK_SESSIONS: list[dict] = [
    # --- Sesiones de Ingeniería y Ciencias Exactas ---
    {
        "_student_index": 10,  # Andrés
        "_tutor_index":   0,   # Nicolás
        "_skill_index":   0,   # Estructuras de Datos
        "scheduledAt": datetime(2026, 4, 13, 9, 0, 0, tzinfo=bog_tz),
    },
    {
        "_student_index": 11,  # Camila
        "_tutor_index":   1,   # Laura
        "_skill_index":   2,   # Cálculo Diferencial
        "scheduledAt": datetime(2026, 4, 13, 11, 0, 0, tzinfo=bog_tz),
    },
    {
        "_student_index": 12,  # Jorge
        "_tutor_index":   2,   # Carlos (Física)
        "_skill_index":   4,   # Mecánica Newtoniana
        "scheduledAt": datetime(2026, 4, 14, 14, 0, 0, tzinfo=bog_tz),
    },

    # --- Sesiones de Economía y Administración ---
    {
        "_student_index": 10,  # Andrés
        "_tutor_index":   4,   # Daniela (Economía)
        "_skill_index":   7,   # Microeconomía I
        "scheduledAt": datetime(2026, 4, 14, 16, 0, 0, tzinfo=bog_tz),
    },
    {
        "_student_index": 13,  # Mariana
        "_tutor_index":   6,   # Juliana (Administración)
        "_skill_index":   9,   # Finanzas Corporativas
        "scheduledAt": datetime(2026, 4, 15, 10, 0, 0, tzinfo=bog_tz),
    },

    # --- Sesiones de Humanidades y Derecho ---
    {
        "_student_index": 14,  # Sebastian
        "_tutor_index":   9,   # Santiago (Derecho)
        "_skill_index":   12,  # Derecho Constitucional
        "scheduledAt": datetime(2026, 4, 15, 15, 0, 0, tzinfo=bog_tz),
    },
    {
        "_student_index": 11,  # Camila
        "_tutor_index":   8,   # Valentina (Psicología)
        "_skill_index":   11,  # Psicología Cognitiva
        "scheduledAt": datetime(2026, 4, 16, 13, 0, 0, tzinfo=bog_tz),
    },

    # --- Sesiones Adicionales de Refuerzo ---
    {
        "_student_index": 12,  # Jorge
        "_tutor_index":   5,   # Felipe (Sistemas)
        "_skill_index":   1,   # Desarrollo Móvil
        "scheduledAt": datetime(2026, 4, 17, 8, 0, 0, tzinfo=bog_tz),
    },
    {
        "_student_index": 13,  # Mariana
        "_tutor_index":   3,   # Ana María (Biología)
        "_skill_index":   6,   # Genética Molecular
        "scheduledAt": datetime(2026, 4, 17, 11, 0, 0, tzinfo=bog_tz),
    },
    {
        "_student_index": 14,  # Sebastian
        "_tutor_index":   7,   # Mateo (Mecánica)
        "_skill_index":   10,  # Termodinámica
        "scheduledAt": datetime(2026, 4, 18, 10, 0, 0, tzinfo=bog_tz),
    },
]