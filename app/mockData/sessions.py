# app/mockData/sessions.py

from datetime import datetime, timedelta, timezone
from app.models.enums import SessionStatus

# Configuración de zona horaria para Bogotá (UTC-5)
bog_tz = timezone(timedelta(hours=-5))

"""
NOTA PARA EL SEEDER:
Este archivo solo contiene la estructura lógica. El seeder se encargará de 
transformar estos índices en los objetos denormalizados:
- ParticipantSummary (id, name, profileImageUrl)
- SkillSummary (id, label)
"""

MOCK_SESSIONS: list[dict] = [
    # --- Ingeniería y Ciencias ---
    {
        "_student_index": 10, # Andrés
        "_tutor_index":   0,  # Nicolás (Sistemas)
        "_skill_index":   0,  # Estructuras de Datos
        "price":          25000,
        "scheduledAt":    datetime(2026, 4, 13, 9, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
    {
        "_student_index": 11, # Camila
        "_tutor_index":   1,  # Laura (Matemáticas)
        "_skill_index":   2,  # Cálculo Diferencial
        "price":          20000,
        "scheduledAt":    datetime(2026, 4, 13, 11, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
    {
        "_student_index": 12, # Jorge
        "_tutor_index":   2,  # Carlos (Física)
        "_skill_index":   4,  # Mecánica Newtoniana
        "price":          30000,
        "scheduledAt":    datetime(2026, 4, 14, 14, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },

    # --- Economía y Administración ---
    {
        "_student_index": 10, # Andrés
        "_tutor_index":   4,  # Daniela (Economía)
        "_skill_index":   7,  # Microeconomía I
        "price":          35000,
        "scheduledAt":    datetime(2026, 4, 14, 16, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
    {
        "_student_index": 13, # Mariana
        "_tutor_index":   6,  # Juliana (Administración)
        "_skill_index":   9,  # Finanzas Corporativas
        "price":          28000,
        "scheduledAt":    datetime(2026, 4, 15, 10, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },

    # --- Humanidades y Derecho ---
    {
        "_student_index": 14, # Sebastian
        "_tutor_index":   9,  # Santiago (Derecho)
        "_skill_index":   12, # Derecho Constitucional
        "price":          32000,
        "scheduledAt":    datetime(2026, 4, 15, 15, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
    {
        "_student_index": 11, # Camila
        "_tutor_index":   8,  # Valentina (Psicología)
        "_skill_index":   11, # Psicología Cognitiva
        "price":          20000,
        "scheduledAt":    datetime(2026, 4, 16, 13, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },

    # --- Refuerzo y Especialidades ---
    {
        "_student_index": 12, # Jorge
        "_tutor_index":   5,  # Felipe (Sistemas)
        "_skill_index":   1,  # Desarrollo Móvil
        "price":          22000,
        "scheduledAt":    datetime(2026, 4, 17, 8, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
    {
        "_student_index": 13, # Mariana
        "_tutor_index":   3,  # Ana María (Biología)
        "_skill_index":   6,  # Genética Molecular
        "price":          18000,
        "scheduledAt":    datetime(2026, 4, 17, 11, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
    {
        "_student_index": 14, # Sebastian
        "_tutor_index":   7,  # Mateo (Mecánica)
        "_skill_index":   10, # Termodinámica
        "price":          26000,
        "scheduledAt":    datetime(2026, 4, 18, 10, 0, 0, tzinfo=bog_tz),
        "status":         SessionStatus.PENDIENTE,
    },
]