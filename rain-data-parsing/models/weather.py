"""Weather and precipitation models."""

from pydantic import BaseModel


class ThunderResponse(BaseModel):
    """Response model for thunder/lightning and rain data."""
    city: str
    latitude: float
    longitude: float
    lightning_probability: int
    rain: float
    timezone: str
    time: str
