# app/mockData/seeder.py

from datetime import datetime, timezone
from google.cloud.firestore_v1 import AsyncClient
from app.mockData.users    import MOCK_USERS
from app.mockData.skills   import MOCK_SKILLS
from app.mockData.reviews  import MOCK_REVIEWS
from app.mockData.sessions import MOCK_SESSIONS
from app.mockData.pqrs     import MOCK_PQRS
from app.repositories.sessions_repository import _generate_verif_code

SEEDED_IDS: dict[str, list[str]] = {
    "users": [], "skills": [], "reviews": [], "sessions": [], "pqrs": []
}


async def seed(db: AsyncClient):
    """Pobla Firestore con datos de prueba al iniciar el servidor."""

    # ------------------------------------------------------------------ Skills
    for skill_data in MOCK_SKILLS:
        ref = db.collection("skills").document()
        await ref.set({**skill_data, "major": skill_data["major"].value})
        SEEDED_IDS["skills"].append(ref.id)

    # ------------------------------------------------------------------ Users
    # Asignar skills a tutores según su carrera
    skill_map: dict[str, list[str]] = {}
    for idx, skill_id in enumerate(SEEDED_IDS["skills"]):
        major_val = MOCK_SKILLS[idx]["major"].value
        skill_map.setdefault(major_val, []).append(skill_id)

    for user_data in MOCK_USERS:
        data = {**user_data, "major": user_data["major"].value}
        if data["isTutoring"]:
            data["tutoringSkills"] = skill_map.get(data["major"], [])
        data["availability"] = {
            day: [ts if isinstance(ts, datetime) else datetime.fromisoformat(ts)
                for ts in slots]
            for day, slots in data["availability"].items()
        }
        ref = db.collection("users").document()
        await ref.set(data)
        SEEDED_IDS["users"].append(ref.id)

    # Actualizar favTutors: Andrés tiene a Nicolás y Laura como favoritos
    await db.collection("users").document(SEEDED_IDS["users"][2]).update({
        "favTutors": [SEEDED_IDS["users"][0], SEEDED_IDS["users"][1]],
        "interestedSkills": SEEDED_IDS["skills"][:2],
    })

    # ------------------------------------------------------------------ Sessions
    for session_data in MOCK_SESSIONS:
        skill_doc = db.collection("skills").document(
            SEEDED_IDS["skills"][session_data["_skill_index"]]
        )
        skill_full = (await skill_doc.get()).to_dict()
        
        ref = db.collection("sessions").document()
        await ref.set({
            "studentId":   SEEDED_IDS["users"][session_data["_student_index"]],
            "tutorId":     SEEDED_IDS["users"][session_data["_tutor_index"]],
            "skill":       skill_full,        # ← objeto completo del skill
            "scheduledAt": session_data["scheduledAt"],
            "status":      "Pendiente",
            "verifCode":   _generate_verif_code(),
        })
        SEEDED_IDS["sessions"].append(ref.id)

    # ------------------------------------------------------------------ Reviews
    # Las reviews referencian sesiones ya concluidas — marcamos la primera como Concluida
    await db.collection("sessions").document(SEEDED_IDS["sessions"][0]).update({
        "status": "Concluida"
    })
    for review_data in MOCK_REVIEWS:
        ref = db.collection("reviews").document()
        await ref.set({
            "authorId":  SEEDED_IDS["users"][review_data["_author_index"]],
            "tutorId":   SEEDED_IDS["users"][review_data["_tutor_index"]],
            "rating":    review_data["rating"],
            "label":     review_data["label"],
            "details":   review_data["details"],
            "createdAt": datetime.now(timezone.utc),
        })
        SEEDED_IDS["reviews"].append(ref.id)

    # ------------------------------------------------------------------ PQRs
    for pqr_data in MOCK_PQRS:
        related = (
            SEEDED_IDS["sessions"][pqr_data["_session_index"]]
            if pqr_data["_session_index"] is not None else None
        )
        ref = db.collection("pqrs").document()
        await ref.set({
            "authorId":        SEEDED_IDS["users"][pqr_data["_author_index"]],
            "type":            pqr_data["type"].value,
            "status":          "Pendiente",
            "topic":           pqr_data["topic"],
            "description":     pqr_data["description"],
            "createdAt":       datetime.now(timezone.utc),
            "relatedIncident": related,
        })
        SEEDED_IDS["pqrs"].append(ref.id)

    print(f"✅ Seeder completado: {SEEDED_IDS}")


async def unseed(db: AsyncClient):
    """Elimina todos los documentos creados por el seeder al cerrar el servidor."""
    for collection, ids in SEEDED_IDS.items():
        for doc_id in ids:
            await db.collection(collection).document(doc_id).delete()
    print("🧹 Unseed completado: datos de prueba eliminados.")
