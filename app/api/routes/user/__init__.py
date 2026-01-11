from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.domain.services import user_service
from app.infrastructure.database import User

from .schema import UserModel

router = APIRouter(tags=["User"], prefix="/users")


@router.get(
    "/me",
    response_model=UserModel,
    summary="Get information about the current user",
    description="Returns information about the current authenticated user",
    response_description="User object",
)
async def me(current_user: Annotated[User, Depends(security.get_current_user)]):
    return UserModel.model_validate(
        current_user,
        from_attributes=True,
    )


@router.get(
    "/{user_id}",
    response_model=UserModel,
    summary="Get user by ID",
    description="Returns information about a user by the specified ID. "
    "The user must belong to the same customer as the current user.",
    response_description="User object with detailed information",
    responses={
        200: {"description": "The user was successfully found"},
        404: {"description": "The user was not found or Access denied"},
    },
)
async def get_user(
    user_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
):
    request_user = await user_service.get_if_available(
        current_user_id=current_user.id,
        user_id=user_id,
    )
    if request_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user was not found or Access denied",
        )
    return UserModel.model_validate(
        request_user,
        from_attributes=True,
    )
