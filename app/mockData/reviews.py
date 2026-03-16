# app/mockData/reviews.py

MOCK_REVIEWS: list[dict] = [
    # author_id y tutor_id se resuelven dinámicamente en el seeder
    {
        "_author_index": 2,   # Andrés → Nicolás
        "_tutor_index":  0,
        "rating":  4.5,
        "label":   "Muy buena explicación",
        "details": "Nicolás explicó Estructuras de Datos de forma muy clara.",
    },
    {
        "_author_index": 2,   # Andrés → Laura
        "_tutor_index":  1,
        "rating":  5.0,
        "label":   "Excelente tutora",
        "details": "Laura domina Cálculo y es muy paciente.",
    },
]
