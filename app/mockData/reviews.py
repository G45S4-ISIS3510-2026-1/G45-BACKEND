
# app/mockData/reviews.py

MOCK_REVIEWS: list[dict] = [
    # --- Tutor 0: Nicolás Ballén (Ing. Sistemas) ---
    {
        "_author_index": 10, "_tutor_index": 0, "rating": 4.5, "label": "Muy buena explicación",
        "details": "Nicolás explicó Estructuras de Datos de forma muy clara.",
    },
    {
        "_author_index": 11, "_tutor_index": 0, "rating": 5.0, "label": "Pro en algoritmos",
        "details": "Me salvó el parcial de algoritmos, muy recomendado.",
    },
    {
        "_author_index": 12, "_tutor_index": 0, "rating": 4.0, "label": "Buen dominio",
        "details": "Conoce mucho del tema, aunque a veces va un poco rápido.",
    },

    # --- Tutor 1: Laura Martínez (Matemáticas) ---
    {
        "_author_index": 10, "_tutor_index": 1, "rating": 5.0, "label": "Excelente tutora",
        "details": "Laura domina Cálculo y es muy paciente.",
    },
    {
        "_author_index": 13, "_tutor_index": 1, "rating": 4.8, "label": "Paciencia increíble",
        "details": "Hace que los temas de Álgebra Lineal parezcan fáciles.",
    },
    {
        "_author_index": 14, "_tutor_index": 1, "rating": 5.0, "label": "La mejor",
        "details": "Puntual y muy clara con los ejercicios prácticos.",
    },

    # --- Tutor 2: Carlos Rodríguez (Física) ---
    {
        "_author_index": 11, "_tutor_index": 2, "rating": 4.2, "label": "Buena metodología",
        "details": "Explica bien las fórmulas de mecánica.",
    },
    {
        "_author_index": 12, "_tutor_index": 2, "rating": 5.0, "label": "Excelente disposición",
        "details": "Resolvió todas mis dudas de laboratorio.",
    },
    {
        "_author_index": 14, "_tutor_index": 2, "rating": 4.5, "label": "Recomendado",
        "details": "Tiene mucho material de apoyo para estudiar.",
    },

    # --- Tutor 3: Ana María Silva (Biología) ---
    {
        "_author_index": 13, "_tutor_index": 3, "rating": 4.9, "label": "Muy apasionada",
        "details": "Se nota que ama la genética, explica con mucho detalle.",
    },
    {
        "_author_index": 10, "_tutor_index": 3, "rating": 4.0, "label": "Buen apoyo",
        "details": "Me ayudó a entender conceptos complejos de molecular.",
    },
    {
        "_author_index": 12, "_tutor_index": 3, "rating": 5.0, "label": "Súper clara",
        "details": "Utiliza muchos ejemplos visuales que ayudan mucho.",
    },

    # --- Tutor 4: Daniela Ospina (Economía) ---
    {
        "_author_index": 10, "_tutor_index": 4, "rating": 5.0, "label": "Dominio total",
        "details": "La mejor para Microeconomía, no hay duda.",
    },
    {
        "_author_index": 14, "_tutor_index": 4, "rating": 4.7, "label": "Muy práctica",
        "details": "Explica los gráficos de una manera muy sencilla.",
    },
    {
        "_author_index": 11, "_tutor_index": 4, "rating": 4.5, "label": "Gran ayuda",
        "details": "Gracias a ella pasé el examen final de Econometría.",
    },

    # --- Tutor 5: Felipe Caicedo (Ing. Sistemas) ---
    {
        "_author_index": 12, "_tutor_index": 5, "rating": 5.0, "label": "Crack en Flutter",
        "details": "Me ayudó con la integración de Firebase, sabe demasiado.",
    },
    {
        "_author_index": 13, "_tutor_index": 5, "rating": 4.3, "label": "Buen tutor",
        "details": "Explica bien los widgets y la lógica de estado.",
    },
    {
        "_author_index": 10, "_tutor_index": 5, "rating": 4.8, "label": "Muy metódico",
        "details": "Te enseña a organizar el código de forma profesional.",
    },

    # --- Tutor 6: Juliana Herrera (Administración) ---
    {
        "_author_index": 13, "_tutor_index": 6, "rating": 5.0, "label": "Claridad financiera",
        "details": "Las finanzas corporativas ya no son un dolor de cabeza.",
    },
    {
        "_author_index": 11, "_tutor_index": 6, "rating": 4.6, "label": "Muy profesional",
        "details": "Llega preparada con ejercicios reales de la clase.",
    },
    {
        "_author_index": 14, "_tutor_index": 6, "rating": 4.9, "label": "Excelente",
        "details": "Juliana es muy organizada y explica paso a paso.",
    },

    # --- Tutor 7: Mateo Londoño (Ing. Mecánica) ---
    {
        "_author_index": 14, "_tutor_index": 7, "rating": 4.1, "label": "Sabe mucho",
        "details": "Termodinámica es difícil pero él lo hace entendible.",
    },
    {
        "_author_index": 12, "_tutor_index": 7, "rating": 4.5, "label": "Práctico",
        "details": "Muchos tips para resolver problemas de energía.",
    },
    {
        "_author_index": 10, "_tutor_index": 7, "rating": 5.0, "label": "Salva materias",
        "details": "Sin su ayuda no habría pasado el parcial.",
    },

    # --- Tutor 8: Valentina Ruiz (Psicología) ---
    {
        "_author_index": 11, "_tutor_index": 8, "rating": 5.0, "label": "Súper recomendada",
        "details": "Tiene una paciencia de oro y domina los temas cognitivos.",
    },
    {
        "_author_index": 13, "_tutor_index": 8, "rating": 4.8, "label": "Muy atenta",
        "details": "Te escucha y adapta la sesión a lo que necesitas.",
    },
    {
        "_author_index": 14, "_tutor_index": 8, "rating": 4.7, "label": "Dinámica",
        "details": "Hace que las lecturas pesadas sean fáciles de digerir.",
    },

    # --- Tutor 9: Santiago Peña (Derecho) ---
    {
        "_author_index": 14, "_tutor_index": 9, "rating": 5.0, "label": "Excelente oratoria",
        "details": "Explica la constitución con una claridad impresionante.",
    },
    {
        "_author_index": 10, "_tutor_index": 9, "rating": 4.4, "label": "Gran dominio legal",
        "details": "Me ayudó a entender la jerarquía normativa de una vez por todas.",
    },
    {
        "_author_index": 13, "_tutor_index": 9, "rating": 4.9, "label": "Puntual y claro",
        "details": "Muy buen apoyo para preparar debates de clase.",
    },
]
