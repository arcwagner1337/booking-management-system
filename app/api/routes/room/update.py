"""PATCH /api/rooms/{id} - Partial update of room data."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.infrastructure.database.models.users import User

from .schema import RoomResponse, RoomUpdate

router = APIRouter()


@router.patch(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Partial update of room data",
)
async def update_room(
    room_id: int,
    room_in: RoomUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Update room data (partial update).

    User must be owner or admin of the customer that owns this resource.
    Only provided fields will be updated.
    """
    update_data = room_in.model_dump(exclude_unset=True)

    resource = await resource_service.update_resource(
        resource_id=room_id,
        current_user=current_user,
        session=session,
        **update_data,
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found or access denied",
        )

    return resource
