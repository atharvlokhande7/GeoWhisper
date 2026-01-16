from pydantic import BaseModel
from typing import List, Optional

class POIData(BaseModel):
    name: str
    category: str
    lat: float
    lon: float

class AIInsight(BaseModel):
    text: str
    audio_friendly: str

class InsightResponse(BaseModel):
    location_received: bool
    significant_move: bool
    movement_type: Optional[str] = None
    nearby_pois: List[POIData] = []
    ai_insight: Optional[AIInsight] = None
