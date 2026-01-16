import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.poi import POI

# Mocking external API for stability/no-key requirement
class POIService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_nearby_pois(self, lat: float, lon: float):
        # In a real app, check DB cache first using PostGIS or bounding box query
        # Here we will just perform a mock external fetch
        
        # Real implementation would be:
        # async with httpx.AsyncClient() as client:
        #    resp = await client.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}")
        
        # Mock Response
        return [
            {"name": "Eiffel Tower (Mock)", "category": "landmark", "lat": lat + 0.001, "lon": lon + 0.001},
            {"name": "Seine River (Mock)", "category": "nature", "lat": lat - 0.001, "lon": lon - 0.001}
        ]
