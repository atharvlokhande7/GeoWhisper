from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.location import LocationUpdate
from app.schemas.response import InsightResponse, POIData, AIInsight
from app.services.location_service import LocationService
from app.services.poi_service import POIService
from app.services.ai_service import AIService
from app.core.database import get_db
import traceback

router = APIRouter()

@router.post("", response_model=InsightResponse)
async def update_location(
    location_data: LocationUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Manual Instantiation
        location_service = LocationService(db)
        poi_service = POIService(db)
        ai_service = AIService()

        # 1. Save Location
        significant, location = await location_service.update_location(
            location_data.user_id,
            location_data.latitude,
            location_data.longitude,
            location_data.speed
        )
        
        # 2. Key/Significant Movement Check
        is_significant = significant
        
        if not location:
             # Handle logic if needed
             pass
        
        lat = location.latitude if location else location_data.latitude
        lon = location.longitude if location else location_data.longitude
        movement_type = location.movement_type if location else "stationary"

        # 3. Fetch POIs
        pois = await poi_service.fetch_nearby_pois(lat, lon)

        # 4. Generate Insight
        insight = await ai_service.generate_insight(
            lat, 
            lon, 
            movement_type,
            pois
        )
        
        return InsightResponse(
            location_received=True,
            significant_move=is_significant,
            movement_type=movement_type,
            nearby_pois=[
                POIData(name=p['name'], category=p['category'], lat=p['lat'], lon=p['lon']) 
                for p in pois
            ],
            ai_insight=AIInsight(**insight)
        )
    except Exception as e:
        # Proper logging implementation later
        traceback.print_exc()
        raise e
