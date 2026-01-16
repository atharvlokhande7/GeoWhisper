import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.poi import POI
from app.utils.redis_client import get_redis
from app.utils.osm_client import OSMClient
from app.core.config import settings

class POIService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.osm_client = OSMClient()

    async def fetch_nearby_pois(self, lat: float, lon: float):
        if not settings.USE_REAL_POIS:
            return self._get_mock_pois(lat, lon)

        # 1. Check Redis Cache (Geospatial or cell-based)
        # Using simple cell-based caching to avoid complex GeoRediSearch setup for now
        # Key: pois:lat_rounded:lon_rounded (approx 100m grid)
        grid_lat = round(lat, 3)
        grid_lon = round(lon, 3)
        cache_key = f"pois:{grid_lat}:{grid_lon}"
        
        redis = await get_redis()
        cached_data = await redis.get(cache_key)
        
        if cached_data:
            return json.loads(cached_data)

        # 2. Fetch from OSM
        pois = await self.osm_client.fetch_pois(lat, lon)
        
        # 3. Cache & Normalize
        if not pois:
           # Fallback to mock if OSM fails or returns nothing, 
           # ensuring the user always gets *something* (demo friendly)
           return self._get_mock_pois(lat, lon)
        
        await redis.setex(cache_key, 3600, json.dumps(pois)) # Cache for 1 hour
        
        # 4. Async save to DB (Fire and forget style ideally, but await here for simplicity)
        # We won't block response on DB writes in v1, 
        # but could persist for offline analytics.
        
        return pois

    def _get_mock_pois(self, lat: float, lon: float):
        return [
            {"name": "Eiffel Tower (Mock)", "category": "landmark", "lat": lat + 0.001, "lon": lon + 0.001},
            {"name": "Seine River (Mock)", "category": "nature", "lat": lat - 0.001, "lon": lon - 0.001}
        ]
