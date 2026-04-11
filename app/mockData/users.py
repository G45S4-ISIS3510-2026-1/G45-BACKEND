from app.models.user import User, Availability, PaymentMethod
from app.models.enums import UniandesMajor

mockImage="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxGhXTEp-G9Z1SBNez2KK6gAeeIbMfRgz-FQ&s"

# Función auxiliar para generar disponibilidad máxima (07:00 a 20:00)
def get_max_availability():
    hours = [f"{h:02d}:00:00" for h in range(7, 21)]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    # Nota: Se usa una fecha base de referencia (ej. marzo 2026) como en tus mocks originales
    return {day: [f"2026-03-20T{hour}" for hour in hours] for day in days}

MAX_AVAIL = get_max_availability()
EMPTY_AVAIL = {"monday": [], "tuesday": [], "wednesday": [], "thursday": [], "friday": [], "saturday": []}

MOCK_USERS: list[dict] = [
    # --- TUTORES (10) con Disponibilidad Máxima ---
    {
        "name": "Nicolás Ballén",
        "email": "nbalenciaga23@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "isTutoring": True,
        "uniandesId": 202012345,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "sessionPrice": 25000,
        "profileImageUrl": mockImage,
        "availability": MAX_AVAIL,
        "paymentMethods": [{"number": "4111...", "cvv": "123", "holder": "Nicolás Ballén", "exp_month": 12, "exp_year": 2028}],
    },
    {
        "name": "Laura Martínez",
        "email": "l.martinez@uniandes.edu.co",
        "major": UniandesMajor.MATEMATICAS,
        "isTutoring": True,
        "uniandesId": 202054321,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage,
        "sessionPrice": 20000,
        "availability": MAX_AVAIL,
        "paymentMethods": [],
    },
    {
        "name": "Carlos Rodríguez", "email": "c.rodriguez@uniandes.edu.co",
        "major": UniandesMajor.FISICA, "isTutoring": True, "uniandesId": 202110101,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 30000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Ana María Silva", "email": "am.silva@uniandes.edu.co",
        "major": UniandesMajor.BIOLOGIA, "isTutoring": True, "uniandesId": 201922334,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 18000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Daniela Ospina", "email": "d.ospina@uniandes.edu.co",
        "major": UniandesMajor.ECONOMIA, "isTutoring": True, "uniandesId": 202230405,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 35000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Felipe Caicedo", "email": "f.caicedo@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_SISTEMAS, "isTutoring": True, "uniandesId": 202115987,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 22000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Juliana Herrera", "email": "j.herrera@uniandes.edu.co",
        "major": UniandesMajor.ADMINISTRACION, "isTutoring": True, "uniandesId": 202028471,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 28000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Mateo Londoño", "email": "m.londono@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_MECANICA, "isTutoring": True, "uniandesId": 201829384,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 26000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Valentina Ruiz", "email": "v.ruiz@uniandes.edu.co",
        "major": UniandesMajor.PSICOLOGIA, "isTutoring": True, "uniandesId": 202138472,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 20000, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Santiago Peña", "email": "s.pena@uniandes.edu.co",
        "major": UniandesMajor.DERECHO, "isTutoring": True, "uniandesId": 202047293,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 32000, "availability": MAX_AVAIL, "paymentMethods": [],
    },

    # --- ESTUDIANTES (5) ---
    {
        "name": "Andrés Gómez", "email": "a.gomez@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_INDUSTRIAL, "isTutoring": False, "uniandesId": 202067890,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 0, "availability": EMPTY_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Camila Torres", "email": "c.torres@uniandes.edu.co",
        "major": UniandesMajor.ARQUITECTURA, "isTutoring": False, "uniandesId": 202210293,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 0, "availability": EMPTY_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Jorge Eliécer", "email": "j.eliecer@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_CIVIL, "isTutoring": False, "uniandesId": 202129384,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 0, "availability": EMPTY_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Mariana Vélez", "email": "m.velez@uniandes.edu.co",
        "major": UniandesMajor.MEDICINA, "isTutoring": False, "uniandesId": 202319482,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 0, "availability": EMPTY_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Sebastian Castro", "email": "s.castro@uniandes.edu.co",
        "major": UniandesMajor.FILOSOFIA, "isTutoring": False, "uniandesId": 202039485,
        "fcmTokens": [], "favTutors": [], "tutoringSkills": [], "interestedSkills": [],
        "profileImageUrl": mockImage, "sessionPrice": 0, "availability": EMPTY_AVAIL, "paymentMethods": [],
    },
]