# app/mockData/seeder.py

from datetime import datetime, timezone, timedelta
import random
from google.cloud.firestore_v1 import AsyncClient
from app.mockData.users    import MOCK_USERS
from app.mockData.skills   import MOCK_SKILLS
from app.mockData.reviews  import MOCK_REVIEWS
from app.mockData.sessions import MOCK_SESSIONS
from app.mockData.pqrs     import MOCK_PQRS
from app.repositories.sessions_repository import _generate_verif_code


# URL de ejemplo (una API de prueba)
url = "https://randomuser.me/api/portraits/med/"
options=["men", "women"]
image_range = range(1, 76)  # Imágenes del 1 al 75

def get_random_image_url():
    gender = random.choice(options)
    image_number = random.choice(image_range)
    return f"{url}{gender}/{image_number}.jpg"

async def seed(db: AsyncClient):
    """Pobla Firestore siguiendo los esquemas de modelos denormalizados."""
    
    # 1. VERIFICACIÓN DE IDEMPOTENCIA
    # Si ya existen usuarios, no ejecutamos el seeder.
    existing_users = await db.collection("users").limit(1).get()
    if len(existing_users) > 0:
        print("⏭️  Base de datos ya inicializada. Saltando seeder.")
        return

    print("🚀 Iniciando carga inicial de datos...")
    bogota_offset = timezone(timedelta(hours=-5))
    
    # Mapeos para mantener integridad referencial entre mocks
    skill_index_to_id = {}
    user_index_to_id = {}
    session_index_to_id = {}

    # ------------------------------------------------------------------ 1. SKILLS
    print("🌱 Cargando Skills...")
    for idx, skill_data in enumerate(MOCK_SKILLS):
        ref = db.collection("skills").document()
        await ref.set({**skill_data, "major": skill_data["major"].value})
        skill_index_to_id[idx] = ref.id

    # Mapa de skills por carrera para asignación automática a tutores
    skill_map_by_major = {}
    for idx, skill_id in skill_index_to_id.items():
        major_val = MOCK_SKILLS[idx]["major"].value
        skill_map_by_major.setdefault(major_val, []).append(skill_id)

    # ------------------------------------------------------------------ 2. USERS
    print("👤 Cargando Usuarios...")
    for idx, user_data in enumerate(MOCK_USERS):
        data = {**user_data, "major": user_data["major"].value}
        
        # Asignar tutoringSkills si es tutor basándose en su major
        if data.get("isTutoring"):
            data["tutoringSkills"] = skill_map_by_major.get(data["major"], [])
        
        # Convertir strings de disponibilidad a datetime objetos
        if "availability" in data:
            data["availability"] = {
                day: [
                    ts if isinstance(ts, datetime) else datetime.fromisoformat(ts).replace(tzinfo=bogota_offset)
                    for ts in slots
                ]
                for day, slots in data["availability"].items()
            }
        
        data["profileImageUrl"] = get_random_image_url()
        
        ref = db.collection("users").document()
        await ref.set(data)
        user_index_to_id[idx] = ref.id

    # ------------------------------------------------------------------ 3. SESSIONS
    print("📅 Generando Sesiones (con resúmenes embebidos)...")
    for idx, session_data in enumerate(MOCK_SESSIONS):
        student_idx = session_data["_student_index"]
        tutor_idx   = session_data["_tutor_index"]
        skill_idx   = session_data["_skill_index"]

        # Extraemos datos raw de los mocks para construir los resúmenes (summaries)
        student_raw = MOCK_USERS[student_idx]
        tutor_raw   = MOCK_USERS[tutor_idx]
        skill_raw   = MOCK_SKILLS[skill_idx]

        # Construcción según ParticipantSummary y SkillSummary
        session_document = {
            "price":       session_data["price"],
            "scheduledAt": session_data["scheduledAt"],
            "status":      session_data["status"].value,
            "verifCode":   _generate_verif_code(),
            "skill": {
                "id":    skill_index_to_id[skill_idx],
                "label": skill_raw["label"]
            },
            "student": {
                "id":              user_index_to_id[student_idx],
                "name":            student_raw["name"],
                "profileImageUrl": student_raw.get("profileImageUrl")
            },
            "tutor": {
                "id":              user_index_to_id[tutor_idx],
                "name":            tutor_raw["name"],
                "profileImageUrl": tutor_raw.get("profileImageUrl")
            }
        }

        ref = db.collection("sessions").document()
        await ref.set(session_document)
        session_index_to_id[idx] = ref.id

    # ------------------------------------------------------------------ 4. REVIEWS
    print("⭐️ Cargando Reviews...")
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

    # ------------------------------------------------------------------ 5. PQRS
    print("📩 Cargando PQRs...")
    for pqr_data in MOCK_PQRS:
        related_session_id = None
        if pqr_data["_session_index"] is not None:
            related_session_id = session_index_to_id.get(pqr_data["_session_index"])

        ref = db.collection("pqrs").document()
        await ref.set({
            "authorId":        user_index_to_id[pqr_data["_author_index"]],
            "type":            pqr_data["type"].value,
            "status":          "Pendiente",
            "topic":           pqr_data["topic"],
            "description":     pqr_data["description"],
            "createdAt":       datetime.now(bogota_offset),
            "relatedIncident": related_session_id,
        })

    print(f"✅ Seeder completado. {len(MOCK_USERS)} usuarios procesados.")