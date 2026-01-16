from typing import List, Dict, Any
from app.services.ai.mock import UnifiedAIProvider
# from app.services.ai.base import AIProvider

class AIService:
    def __init__(self):
        self.provider = UnifiedAIProvider()

    async def generate_insight(
        self, 
        lat: float, 
        lon: float, 
        movement_type: str, 
        pois: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        return await self.provider.generate_insight(lat, lon, movement_type, pois)
