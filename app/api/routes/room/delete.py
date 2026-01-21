"""DELETE /api/rooms/{id} - Delete a room."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.infrastructure.database.models.users import User

router = APIRouter()


@router.delete(
    "/{room_id}",
    summary="Delete a room",
)
async def delete_room(
    room_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Delete a room from the database.

    User must be owner or admin of the customer that owns this resource.

    Note: Currently performs hard delete as model lacks is_active field.
    To implement soft delete, add is_active column via migration.
    """
    success = await resource_service.delete_resource(
        resource_id=room_id,
        current_user=current_user,
        session=session,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found or access denied",
        )

    return {"ok": True}
