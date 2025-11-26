"""Time response models."""

from pydantic import BaseModel


class TimeResponse(BaseModel):
    """Response model for time endpoint."""
    ticks: int
