"""
POST /api/rooms - Создание комнаты для брони

Исполнитель: [ИМЯ]
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.booking import Resource
from app.infrastructure.database.models.users import User

from .schema import RoomCreate, RoomResponse

router = APIRouter()


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание комнаты для брони",
)
async def create_room(
    data: RoomCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Создание новой комнаты (ресурса).
    """
    resource = Resource(customer_id=data.customer_id, name=data.name)
    session.add(resource)

    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid customer_id (customer not found)",
        ) from err

    await session.refresh(resource)
    return resource
