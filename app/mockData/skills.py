# app/mockData/skills.py

from app.models.enums import UniandesMajor

MOCK_SKILLS: list[dict] = [
    {
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "label": "Estructuras de Datos",
        "iconUrl": "https://cdn.example.com/icons/data-structures.png",
    },
    {
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "label": "Algoritmos y Complejidad",
        "iconUrl": "https://cdn.example.com/icons/algorithms.png",
    },
    {
        "major": UniandesMajor.MATEMATICAS,
        "label": "Cálculo Diferencial",
        "iconUrl": "https://cdn.example.com/icons/calculus.png",
    },
    {
        "major": UniandesMajor.MATEMATICAS,
        "label": "Álgebra Lineal",
        "iconUrl": "https://cdn.example.com/icons/linear-algebra.png",
    },
    {
        "major": UniandesMajor.INGENIERIA_INDUSTRIAL,
        "label": "Investigación de Operaciones",
        "iconUrl": "https://cdn.example.com/icons/operations.png",
    },
]
