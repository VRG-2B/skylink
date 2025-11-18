"""Weather and precipitation models."""

from pydantic import BaseModel


class ThunderResponse(BaseModel):
    """Response model for thunder/lightning data."""
    city: str
    latitude: float
    longitude: float
    lightning_probability: int
    timezone: str
    time: str
