# app/mockData/users.py

from app.models.user import User, Availability, PaymentMethod
from app.models.enums import UniandesMajor

MOCK_USERS: list[dict] = [
    {
        "name": "Nicolás Ballén",
        "email": "n.ballen@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_SISTEMAS,
        "isTutoring": True,
        "uniandesId": 202012345,
        "tutorRating": 4.5,
        "receivedRatings": 1,
        "fcmTokens": [],
        "favTutors": [],
        "tutoringSkills": [],   # se llenan tras insertar skills
        "interestedSkills": [],
        "sessionPrice": 25000,
        "profileImageUrl": "https://i.pravatar.cc/150?u=nicolas",
        "availability": {
            "monday":    ["2026-03-16T09:00:00", "2026-03-16T11:00:00"],
            "tuesday":   [],
            "wednesday": ["2026-03-18T14:00:00","2026-03-18T15:00:00", "2026-03-18T16:00:00", "2026-03-18T17:00:00"],
            "thursday":  [],
            "friday":    ["2026-03-20T10:00:00"],
            "saturday":  [],
        },
        "paymentMethods": [
            {
                "number": "4111111111111111",
                "cvv": "123",
                "holder": "Nicolás Ballén",
                "exp_month": 12,
                "exp_year": 2028,
            }
        ],
    },
    {
        "name": "Laura Martínez",
        "email": "l.martinez@uniandes.edu.co",
        "major": UniandesMajor.MATEMATICAS,
        "isTutoring": True,
        "uniandesId": 202054321,
        "tutorRating": 5.0,
        "receivedRatings": 1,
        "fcmTokens": [],
        "favTutors": [],
        "tutoringSkills": [],
        "interestedSkills": [],
        "profileImageUrl": "https://i.pravatar.cc/150?u=laura",
        "sessionPrice": 20000,
        "availability": {
            "monday":    ["2026-03-16T08:00:00"],
            "tuesday":   ["2026-03-17T10:00:00"],
            "wednesday": [],
            "thursday":  ["2026-03-19T15:00:00"],
            "friday":    [],
            "saturday":  ["2026-03-21T09:00:00", "2026-03-21T10:00:00", "2026-03-21T11:00:00"],
        },
        "paymentMethods": [],
    },
    {
        "name": "Andrés Gómez",
        "email": "a.gomez@uniandes.edu.co",
        "major": UniandesMajor.INGENIERIA_INDUSTRIAL,
        "isTutoring": False,
        "uniandesId": 202067890,
        "tutorRating": 0,
        "receivedRatings": 0,
        "fcmTokens": [],
        "favTutors": [],
        "tutoringSkills": [],
        "interestedSkills": [],
        "profileImageUrl": "https://i.pravatar.cc/150?u=andres",
        "sessionPrice": 0,
        "availability": {
            "monday": [], "tuesday": [], "wednesday": [],
            "thursday": [], "friday": [], "saturday": [],
        },
        "paymentMethods": [],
    },
]
