# app/mockData/seeder.py

from datetime import datetime, timezone, timedelta
from google.cloud.firestore_v1 import AsyncClient
from app.mockData.users    import MOCK_USERS
from app.mockData.skills   import MOCK_SKILLS
from app.mockData.reviews  import MOCK_REVIEWS
from app.mockData.sessions import MOCK_SESSIONS
from app.mockData.pqrs     import MOCK_PQRS
from app.repositories.sessions_repository import _generate_verif_code

async def seed(db: AsyncClient):
    """Pobla Firestore solo si la base de datos está vacía."""
    
    # 1. VERIFICACIÓN DE PRE-VUELO
    # Si ya existe al menos un usuario, asumimos que el sistema ya fue seeded.
    existing_users = await db.collection("users").limit(1).get()
    if len(existing_users) > 0:
        print("⏭️  Base de datos ya contiene datos. Saltando seeder para evitar duplicados.")
        return

    print("🚀 Iniciando carga inicial de datos (Seeding)...")
    bogota_offset = timezone(timedelta(hours=-5))
    
    # Diccionarios para mapear indices de mockData -> IDs reales de Firestore
    skill_index_to_id = {}
    user_index_to_id = {}
    session_index_to_id = {}

    # ------------------------------------------------------------------ 1. Skills
    for idx, skill_data in enumerate(MOCK_SKILLS):
        ref = db.collection("skills").document()
        await ref.set({**skill_data, "major": skill_data["major"].value})
        skill_index_to_id[idx] = ref.id

    # Mapa de skills por carrera
    skill_map_by_major = {}
    for idx, skill_id in skill_index_to_id.items():
        major_val = MOCK_SKILLS[idx]["major"].value
        skill_map_by_major.setdefault(major_val, []).append(skill_id)

    # ------------------------------------------------------------------ 2. Users
    for idx, user_data in enumerate(MOCK_USERS):
        data = {**user_data, "major": user_data["major"].value}
        
        if data["isTutoring"]:
            data["tutoringSkills"] = skill_map_by_major.get(data["major"], [])
        
        # Formatear disponibilidad
        data["availability"] = {
            day: [ts if isinstance(ts, datetime) else datetime.fromisoformat(ts).replace(tzinfo=bogota_offset)
                for ts in slots]
            for day, slots in data["availability"].items()
        }
        
        ref = db.collection("users").document()
        await ref.set(data)
        user_index_to_id[idx] = ref.id

    # ------------------------------------------------------------------ 3. Sessions
    for idx, session_data in enumerate(MOCK_SESSIONS):
        skill_id = skill_index_to_id[session_data["_skill_index"]]
        skill_doc = await db.collection("skills").document(skill_id).get()
        
        ref = db.collection("sessions").document()
        await ref.set({
            "studentId":   user_index_to_id[session_data["_student_index"]],
            "tutorId":     user_index_to_id[session_data["_tutor_index"]],
            "skill":       skill_doc.to_dict(),
            "scheduledAt": session_data["scheduledAt"],
            "status":      "Pendiente",
            "verifCode":   _generate_verif_code(),
        })
        session_index_to_id[idx] = ref.id

    # ------------------------------------------------------------------ 4. Reviews
    for review_data in MOCK_REVIEWS:
        ref = db.collection("reviews").document()
        await ref.set({
            "authorId":  user_index_to_id[review_data["_author_index"]],
            "tutorId":   user_index_to_id[review_data["_tutor_index"]],
            "rating":    review_data["rating"],
            "label":     review_data["label"],
            "details":   review_data["details"],
            "createdAt": datetime.now(bogota_offset),
        })

    # ------------------------------------------------------------------ 5. PQRs
    for pqr_data in MOCK_PQRS:
        related_id = None
        if pqr_data["_session_index"] is not None:
            related_id = session_index_to_id.get(pqr_data["_session_index"])

        ref = db.collection("pqrs").document()
        await ref.set({
            "authorId":        user_index_to_id[pqr_data["_author_index"]],
            "type":            pqr_data["type"].value,
            "status":          "Pendiente",
            "topic":           pqr_data["topic"],
            "description":     pqr_data["description"],
            "createdAt":       datetime.now(bogota_offset),
            "relatedIncident": related_id,
        })

    print(f"✅ Seeder completado. Se cargaron {len(MOCK_USERS)} usuarios y sus relaciones.")