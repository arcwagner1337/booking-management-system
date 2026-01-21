"""Pydantic schemas for room (resource) operations."""

from datetime import datetime
import uuid

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    """Schema for creating a room (POST /api/rooms)."""

    customer_id: uuid.UUID | None = Field(
        None,
        description="Customer ID. If not provided, uses user's customer.",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Room name",
    )


class RoomUpdate(BaseModel):
    """Schema for partial room update (PATCH /api/rooms/{id})."""

    name: str | None = Field(None, min_length=1, max_length=255)


class RoomResponse(BaseModel):
    """Response schema with room data."""

    id: int
    customer_id: uuid.UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
