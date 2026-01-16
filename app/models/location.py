from sqlalchemy.types import String, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base

class Location(Base):
    __tablename__ = "location_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    speed: Mapped[float] = mapped_column(Float, nullable=True) # Speed in m/s
    movement_type: Mapped[str] = mapped_column(String, nullable=True) # walk, run, drive
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
