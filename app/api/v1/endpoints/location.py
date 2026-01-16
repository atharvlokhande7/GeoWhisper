from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.location import LocationUpdate
from app.schemas.response import InsightResponse, POIData, AIInsight
from app.services.location_service import LocationService
from app.services.poi_service import POIService
from app.services.ai_service import AIService
from app.core.database import get_db

router = APIRouter()

@router.post("/location", response_model=InsightResponse)
async def update_location(
    loc: LocationUpdate,
    db: AsyncSession = Depends(get_db)
):
    loc_service = LocationService(db)
    poi_service = POIService(db)
    ai_service = AIService()

    # 1. Process Location
    significant, location_obj = await loc_service.update_location(
        loc.user_id, loc.latitude, loc.longitude, loc.speed
    )

    if not significant:
        return InsightResponse(
            location_received=True,
            significant_move=False
        )

    # 2. Fetch POIs
    pois = await poi_service.fetch_nearby_pois(loc.latitude, loc.longitude)
    
    # 3. Generate Insight
    insight_data = await ai_service.generate_insight(
        loc.latitude, 
        loc.longitude, 
        location_obj.movement_type, 
        pois
    )

    return InsightResponse(
        location_received=True,
        significant_move=True,
        movement_type=location_obj.movement_type,
        nearby_pois=[POIData(**p) for p in pois],
        ai_insight=AIInsight(**insight_data)
    )
