"""
GET /api/rooms/{id} - Получение данных о комнате

Исполнитель: [ИМЯ]
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.booking import Resource
from app.infrastructure.database.models.users import User

from .schema import RoomResponse

router = APIRouter()


@router.get(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Получение данных о комнате",
)
async def read_room(
    room_id: int,
    _current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Получение информации о конкретной комнате по ID.
    """
    stmt = select(Resource).where(Resource.id == room_id)
    result = await session.execute(stmt)
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комната не найдена",
        )

    return room
