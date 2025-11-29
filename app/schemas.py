"""Pydantic schemas for request/response validation."""
from datetime import datetime

from pydantic import BaseModel


class ItemCreate(BaseModel):
    """Schema for creating an item."""

    name: str


class ItemUpdate(BaseModel):
    """Schema for updating an item."""

    name: str | None = None


class ItemResponse(BaseModel):
    """Schema for item response."""

    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
