from typing import Protocol, List, Dict, Any

class AIProvider(Protocol):
    async def generate_insight(
        self, 
        lat: float, 
        lon: float, 
        movement_type: str, 
        pois: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate a short insight.
        Returns: {"text": str, "audio_friendly": str}
        """
        ...
