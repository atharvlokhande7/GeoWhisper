from sqlalchemy.types import String, Float, DateTime, Integer, Text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base

class POI(Base):
    __tablename__ = "pois"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True) # OSM ID
    osm_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True) # AI generated description
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
