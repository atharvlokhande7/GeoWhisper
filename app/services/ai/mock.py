from typing import List, Dict, Any
import random
from datetime import datetime
from app.core.config import settings
# from app.services.ai.base import AIProvider

class UnifiedAIProvider:
    async def generate_insight(
        self, 
        lat: float, 
        lon: float, 
        movement_type: str, 
        pois: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        
        if settings.AI_PROVIDER == "rule_based":
            return self._generate_rule_based(lat, lon, movement_type, pois)
        else:
            return self._generate_mock(lat, lon, movement_type, pois)

    def _generate_mock(self, lat, lon, movement_type, pois):
        poi_names = ", ".join([p['name'] for p in pois[:3]])
        if not poi_names:
            poi_names = "unknown location"

        templates = [
            f"You are currently {movement_type} near {poi_names}. It's a great day for exploration!",
            f"Note the {poi_names} nearby. As you are {movement_type}, take a moment to look around.",
            f"Detected {movement_type}. {poi_names} is close by."
        ]
        
        text = random.choice(templates)
        return {
            "text": text,
            "audio_friendly": text
        }

    def _generate_rule_based(self, lat, lon, movement_type, pois):
        hour = datetime.now().hour
        time_of_day = "day"
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"

        text = ""
        
        if not pois:
            if movement_type == "walking":
                text = f"Enjoying a {time_of_day} walk? Keep exploring!"
            elif movement_type == "cycling":
                text = f"Great {time_of_day} for a ride."
            else:
                text = f"Traveling through the {time_of_day}."
        else:
            primary_poi = pois[0]
            name = primary_poi['name']
            cat = primary_poi['category']
            
            if movement_type == "walking":
                if cat in ["park", "nature"]:
                    text = f"It's a beautiful {time_of_day} for a walk in {name}."
                elif cat in ["cafe", "restaurant", "bar"]:
                    text = f"Walking past {name}. Maybe stop for a bite?"
                elif cat in ["historic", "monument", "landmark"]:
                    text = f"You are near {name}. Take a look at this historic site."
                else:
                    text = f"Walking near {name} ({cat})."
            elif movement_type == "cycling":
                 text = f"Cycling past {name}. Ride safe!"
            elif movement_type == "vehicle":
                 text = f"Passing by {name}."
            else:
                 text = f"You are at {name}."

        return {
            "text": text,
            "audio_friendly": text
        }
