import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.user import User
from app.repositories.user_repository import UserRepository

class RecommenderService:
    def __init__(self, userRepo:UserRepository):
        self.userRepo = userRepo
        
        
    async def load_all_tutors(self):
        tutors= await self.userRepo.get_all_tutors()
        # 1. Convertimos la lista de objetos User a un DataFrame de pandas
        self.df = pd.DataFrame([u.model_dump() for u in tutors if u.is_tutoring])
        
        # 2. Preparamos los "features" (habilidades + carrera)
        # Creamos una cadena de texto que represente al tutor
        self.df['metadata'] = self.df.apply(
            lambda x: f"{' '.join(x['tutoring_skills'])} {x['major']}", axis=1
        )
        
        # 3. Vectorizamos las características
        self.count_vec = CountVectorizer(stop_words=None)
        self.count_matrix = self.count_vec.fit_transform(self.df['metadata'])
        
    async def get_recommendations(self, searched_tutor_ids: list[str], n_top: int = 5):
        """
        Calcula tutores similares basados en una lista de IDs previamente buscados.
        """
        # Filtrar solo IDs válidos que existan en nuestro set de tutores
        valid_indices = self.df[self.df['id'].isin(searched_tutor_ids)].index
        
        if len(valid_indices) == 0:
            return []

        # 4. Creamos el vector promedio de los tutores buscados (Perfil del Usuario)
        user_profile_vector = self.count_matrix[valid_indices].mean(axis=0)
        user_profile_vector = np.asarray(user_profile_vector)
        
        # 5. Calculamos la similitud de todos los tutores contra ese perfil
        cosine_sim = cosine_similarity(user_profile_vector, self.count_matrix)
        
        # 6. Obtenemos los índices de los más similares (excluyendo los ya buscados)
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        recommended_indices = [
            i[0] for i in sim_scores 
            if self.df.iloc[i[0]]['id'] not in searched_tutor_ids
        ]
        valid_ids=self.df.iloc[recommended_indices[:n_top]].to_dict(orient="records")
        recommended_users=[]
        for tutor_id in valid_ids:
            tutor = await self.userRepo.get_by_id(tutor_id['id'])
            if tutor:
                recommended_users.append(tutor)
        
        return recommended_users