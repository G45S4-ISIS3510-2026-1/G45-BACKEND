# app/services/novelties_service.py

from app.repositories.novelty_repository import NoveltiesRepository

class NoveltiesService:
    def __init__(self, repository: NoveltiesRepository):
        self.repository = repository

    async def mark_as_read(self, novelty_id: str) -> bool:
        """
        Lógica de negocio para marcar como leída. 
        Podría retornar False si el ID no existe.
        """
        await self.repository.mark_as_read(novelty_id)
        return True