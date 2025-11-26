"""Precipitation models."""

from pydantic import BaseModel


class PrecipitationResponse(BaseModel):
    """Response model for precipitation endpoint."""
    rain: bool
    thunder: bool
