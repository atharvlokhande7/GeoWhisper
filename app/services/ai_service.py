import random

class AIService:
    @staticmethod
    async def generate_insight(lat: float, lon: float, movement_type: str, pois: list):
        # Mock LLM generation
        
        poi_names = ", ".join([p['name'] for p in pois])
        templates = [
            f"You are currently {movement_type} near {poi_names}. It's a great day for exploration!",
            f"Note the {poi_names} nearby. As you are {movement_type}, take a moment to look around.",
            f"Detected {movement_type}. {poi_names} is close by."
        ]
        
        text = random.choice(templates)
        
        return {
            "text": text,
            "audio_friendly": text  # In real app, might strip abbreviations
        }
