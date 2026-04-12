from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.user import User
from app.repositories.user_repository import UserRepository

class RecommenderService:
    _instance = None
    _last_update = None
    _cache_duration = timedelta(minutes=30)
    _df_cache = None
    _matrix_cache = None
    def __init__(self, userRepo:UserRepository):
        self.count_vec = CountVectorizer(stop_words=None)
        self.userRepo = userRepo
        
    async def _refresh_data_if_needed(self):
        """Consulta la DB solo si el cache expiró o está vacío."""
        now = datetime.now()
        if (RecommenderService._df_cache is None or 
            RecommenderService._last_update is None or 
            (now - RecommenderService._last_update) > RecommenderService._cache_duration):
            
            print("Refrescando cache de tutores desde la base de datos...")
            # 1. Obtener todos los tutores (Asegúrate de usar await aquí)
            tutors = await self.userRepo.get_all_tutors()
            
            # 2. Reconstruir el DataFrame
            data = [u.model_dump(by_alias=True) for u in tutors if u.is_tutoring]
            RecommenderService._df_cache = pd.DataFrame(data)
            
            if not RecommenderService._df_cache.empty:
                # 3. Re-entrenar el vectorizador
                metadata = RecommenderService._df_cache.apply(
                    lambda x: f"{' '.join(x.get('tutoringSkills', []))} {x.get('major', '')}", 
                    axis=1
                )
                RecommenderService._matrix_cache = self.count_vec.fit_transform(metadata)
                RecommenderService._last_update = now
                
        
    async def get_recommendations(self, searched_tutor_ids: list[str], n_top: int = 5):
        """
        Calcula tutores similares basados en una lista de IDs previamente buscados.
        """
        # Primero verificamos si necesitamos actualizar datos
        await self._refresh_data_if_needed()
        
        if RecommenderService._df_cache is None or RecommenderService._df_cache.empty:
            return []
        # Filtrar solo IDs válidos que existan en nuestro set de tutores
        valid_indices = RecommenderService._df_cache[RecommenderService._df_cache['id'].isin(searched_tutor_ids)].index
        
        if len(valid_indices) == 0:
            return []

        # 4. Creamos el vector promedio de los tutores buscados (Perfil del Usuario)
        user_profile_vector = RecommenderService._matrix_cache[valid_indices].mean(axis=0)
        user_profile_vector = np.asarray(user_profile_vector)
        
        # 5. Calculamos la similitud de todos los tutores contra ese perfil
        cosine_sim = cosine_similarity(user_profile_vector, RecommenderService._matrix_cache)
        
        # 6. Obtenemos los índices de los más similares (excluyendo los ya buscados)
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        recommended_indices = [
            i[0] for i in sim_scores 
            if RecommenderService._df_cache.iloc[i[0]]['id'] not in searched_tutor_ids
        ]
        valid_ids=RecommenderService._df_cache.iloc[recommended_indices[:n_top]].to_dict(orient="records")
        recommended_users=[]
        for tutor_id in valid_ids:
            tutor = await self.userRepo.get_by_id(tutor_id['id'])
            if tutor:
                recommended_users.append(tutor)
        
        return recommended_users