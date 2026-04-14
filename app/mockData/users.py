# app/mockData/users.py

from app.models.enums import UniandesMajor

mockImage = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxGhXTEp-G9Z1SBNez2KK6gAeeIbMfRgz-FQ&s"

# Helper para disponibilidad máxima
def get_max_availability_iso():
    hours = [f"{h:02d}:00:00" for h in range(7, 21)]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    return {day: [f"2026-04-13T{hour}" for hour in hours] for day in days}

MAX_AVAIL = get_max_availability_iso()
EMPTY_AVAIL = {"monday": [], "tuesday": [], "wednesday": [], "thursday": [], "friday": [], "saturday": []}

MOCK_USERS: list[dict] = [
    # --- TUTORES (10) ---
    {
        "name": "Nicolás Ballén",
        "email": "nbalenciaga23@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "isTutoring": True,
        "uniandesId": 202012345,
        "sessionPrice": 25000,
        "tutorRating": 4.8,
        "receivedRatings": 15,
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
        "sessionPrice": 20000,
        "tutorRating": 5.0,
        "receivedRatings": 10,
        "profileImageUrl": mockImage,
        "availability": MAX_AVAIL,
        "paymentMethods": [],
    },
    # ... (Agregas los otros 8 tutores siguiendo el patrón de arriba)
    {
        "name": "Carlos Rodríguez", "email": "c.rodriguez@uniandes.edu.co", "major": UniandesMajor.FISICA, 
        "isTutoring": True, "uniandesId": 202110101, "sessionPrice": 30000, "tutorRating": 4.5, "receivedRatings": 8,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Maria Vuitrago", "email": "m.vuitrago@uniandes.edu.co", "major": UniandesMajor.FISICA, 
        "isTutoring": True, "uniandesId": 210231232, "sessionPrice": 30000, "tutorRating": 4.5, "receivedRatings": 8,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Andres Felipe Venimar", "email": "a.felipev@uniandes.edu.co", "major": UniandesMajor.FISICA, 
        "isTutoring": True, "uniandesId": 220301998, "sessionPrice": 30000, "tutorRating": 4.5, "receivedRatings": 8,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Ana María Silva", "email": "am.silva@uniandes.edu.co", "major": UniandesMajor.BIOLOGIA, 
        "isTutoring": True, "uniandesId": 201922334, "sessionPrice": 18000, "tutorRating": 4.9, "receivedRatings": 12,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Daniela Ospina", "email": "d.ospina@uniandes.edu.co", "major": UniandesMajor.ECONOMIA, 
        "isTutoring": True, "uniandesId": 202230405, "sessionPrice": 35000, "tutorRating": 4.7, "receivedRatings": 9,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Felipe Caicedo", "email": "f.caicedo@uniandes.edu.co", "major": UniandesMajor.INGENIERIA_SISTEMAS, 
        "isTutoring": True, "uniandesId": 202115987, "sessionPrice": 22000, "tutorRating": 5.0, "receivedRatings": 5,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Juliana Herrera", "email": "j.herrera@uniandes.edu.co", "major": UniandesMajor.ADMINISTRACION, 
        "isTutoring": True, "uniandesId": 202028471, "sessionPrice": 28000, "tutorRating": 4.6, "receivedRatings": 7,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Mateo Londoño", "email": "m.londono@uniandes.edu.co", "major": UniandesMajor.INGENIERIA_MECANICA, 
        "isTutoring": True, "uniandesId": 201829384, "sessionPrice": 26000, "tutorRating": 4.3, "receivedRatings": 11,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Valentina Ruiz", "email": "v.ruiz@uniandes.edu.co", "major": UniandesMajor.PSICOLOGIA, 
        "isTutoring": True, "uniandesId": 202138472, "sessionPrice": 20000, "tutorRating": 4.9, "receivedRatings": 14,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },
    {
        "name": "Santiago Peña", "email": "s.pena@uniandes.edu.co", "major": UniandesMajor.DERECHO, 
        "isTutoring": True, "uniandesId": 202047293, "sessionPrice": 32000, "tutorRating": 4.4, "receivedRatings": 6,
        "profileImageUrl": mockImage, "availability": MAX_AVAIL, "paymentMethods": [],
    },

    # --- ESTUDIANTES (5) ---
    {
        "name": "Andrés Gómez",
        "email": "a.gomez@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_INDUSTRIAL,
        "isTutoring": False,
        "uniandesId": 202067890,
        "sessionPrice": 0,
        "profileImageUrl": mockImage,
        "availability": EMPTY_AVAIL,
        "paymentMethods": [],
    },
    # ... (Sigue con Camila, Jorge, Mariana y Sebastian igual que el anterior)
    {
        "name": "Camila Torres", "email": "c.torres@uniandes.edu.co", "major": UniandesMajor.ARQUITECTURA,
        "isTutoring": False, "uniandesId": 202210293, "sessionPrice": 0, "profileImageUrl": mockImage, "availability": EMPTY_AVAIL,
    },
    {
        "name": "Jorge Eliécer", "email": "j.eliecer@uniandes.edu.co", "major": UniandesMajor.INGENIERIA_CIVIL,
        "isTutoring": False, "uniandesId": 202129384, "sessionPrice": 0, "profileImageUrl": mockImage, "availability": EMPTY_AVAIL,
    },
    {
        "name": "Mariana Vélez", "email": "m.velez@uniandes.edu.co", "major": UniandesMajor.MEDICINA,
        "isTutoring": False, "uniandesId": 202319482, "sessionPrice": 0, "profileImageUrl": mockImage, "availability": EMPTY_AVAIL,
    },
    {
        "name": "Sebastian Castro", "email": "s.castro@uniandes.edu.co", "major": UniandesMajor.FILOSOFIA,
        "isTutoring": False, "uniandesId": 202039485, "sessionPrice": 0, "profileImageUrl": mockImage, "availability": EMPTY_AVAIL,
    },
]