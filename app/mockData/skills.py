# app/mockData/skills.py

from app.models.enums import UniandesMajor

MOCK_SKILLS: list[dict] = [
    # --- INGENIERÍA DE SISTEMAS ---
    {
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "label": "Estructuras de Datos",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
    },
    {
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "label": "Desarrollo Móvil (Flutter/Kotlin)",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/2586/2586167.png",
    },
    # --- MATEMÁTICAS ---
    {
        "major": UniandesMajor.MATEMATICAS,
        "label": "Cálculo Diferencial",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/3426/3426631.png",
    },
    {
        "major": UniandesMajor.MATEMATICAS,
        "label": "Álgebra Lineal",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/3121/3121810.png",
    },
    # --- FÍSICA ---
    {
        "major": UniandesMajor.FISICA,
        "label": "Mecánica Newtoniana",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/3011/3011119.png",
    },
    {
        "major": UniandesMajor.FISICA,
        "label": "Electromagnetismo",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    },
    # --- BIOLOGÍA ---
    {
        "major": UniandesMajor.BIOLOGIA,
        "label": "Genética Molecular",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/3062/3062331.png",
    },
    # --- ECONOMÍA ---
    {
        "major": UniandesMajor.ECONOMIA,
        "label": "Microeconomía I",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/2761/2761118.png",
    },
    {
        "major": UniandesMajor.ECONOMIA,
        "label": "Econometría",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/4245/4245366.png",
    },
    # --- ADMINISTRACIÓN ---
    {
        "major": UniandesMajor.ADMINISTRACION,
        "label": "Finanzas Corporativas",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/2850/2850341.png",
    },
    # --- INGENIERÍA MECÁNICA ---
    {
        "major": UniandesMajor.INGENIERIA_MECANICA,
        "label": "Termodinámica",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/1835/1835158.png",
    },
    # --- PSICOLOGÍA ---
    {
        "major": UniandesMajor.PSICOLOGIA,
        "label": "Psicología Cognitiva",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/3070/3070713.png",
    },
    # --- DERECHO ---
    {
        "major": UniandesMajor.DERECHO,
        "label": "Derecho Constitucional",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/3406/3406368.png",
    },
    # --- INGENIERÍA INDUSTRIAL ---
    {
        "major": UniandesMajor.INGENIERIA_INDUSTRIAL,
        "label": "Investigación de Operaciones",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/1541/1541415.png",
    },
    {
        "major": UniandesMajor.INGENIERIA_INDUSTRIAL,
        "label": "Logística y Cadenas de Suministro",
        "iconUrl": "https://cdn-icons-png.flaticon.com/512/2830/2830305.png",
    },
]