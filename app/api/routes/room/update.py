"""
PUT /api/rooms/{id} - Обновление данных о комнате

Исполнитель: [ИМЯ]
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.booking import Resource
from app.infrastructure.database.models.users import User

from .schema import RoomResponse, RoomUpdate

router = APIRouter()


@router.put(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Обновление данных о комнате",
)
async def update_room(
    room_id: int,
    room_in: RoomUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Обновление данных комнаты.
    """
    # 1. Найти комнату по ID
    stmt = select(Resource).where(Resource.id == room_id)
    result = await session.execute(stmt)
    room = result.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комната не найдена",
        )

    # 2. Обновить поля из room_in (только те, что переданы)
    update_data = room_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)

    # 3. Сохранить изменения
    await session.commit()
    await session.refresh(room)

    return room
