"""
DELETE /api/rooms/{id} - Удаление (деактивация) комнаты

Исполнитель: [ИМЯ]
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.booking import Resource
from app.infrastructure.database.models.users import User

router = APIRouter()


@router.delete("/{room_id}", summary="Удаление комнаты")
async def delete_room(
    room_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Удаление комнаты из базы данных.

    Примечание: В текущей модели Resource нет поля is_active,
    поэтому выполняется жёсткое удаление.
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

    # 2. Удалить комнату
    await session.delete(room)
    await session.commit()

    return {"ok": True}
