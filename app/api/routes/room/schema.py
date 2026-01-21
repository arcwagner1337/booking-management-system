"""
Pydantic схемы для работы с комнатами (ресурсами).
"""

from datetime import datetime
import uuid

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    """Схема для создания комнаты (POST /api/rooms)."""

    customer_id: uuid.UUID = Field(..., description="ID заказчика")
    name: str = Field(..., min_length=1, max_length=255, description="Название комнаты")


class RoomUpdate(BaseModel):
    """Схема для обновления комнаты (PUT /api/rooms/{id})."""

    name: str | None = Field(None, min_length=1, max_length=255)


class RoomResponse(BaseModel):
    """Схема ответа с данными комнаты."""

    id: int
    customer_id: uuid.UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
