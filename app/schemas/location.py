from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LocationUpdate(BaseModel):
    user_id: str = Field(..., description="Dummy user ID")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    speed: float = Field(0.0, ge=0)
    timestamp: datetime = Field(default_factory=datetime.now)

class LocationResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None
