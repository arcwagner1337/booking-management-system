from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.routes.user.schema import UserModel
from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.user import customer_service
from app.infrastructure.database import Customer, User

from .schema import CustomerModel, CustomerModelCreate

router = APIRouter(tags=["Customer"], prefix="/customers")


@router.get(
    "/{customer_id}",
    response_model=CustomerModel,
    summary="Get information about the current client",
    description=(
        "Returns information about the client to which the current user belongs"
    ),
    response_description="Created customer object",
    responses={
        200: {"description": "The client was successfully found"},
        404: {"description": "The client was not found"},
    },
)
async def get_customer(
    customer_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],  # noqa: ARG001
):
    customer = await Customer.get(id=customer_id)
    if customer:
        return CustomerModel.model_validate(customer, from_attributes=True)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@router.post(
    "/",
    response_model=CustomerModel,
    summary="Create a new customer",
    description="Creates a new customer and binds it to the current user. "
    "The user can create only one customer.",
    response_description="Created customer object",
    responses={
        200: {"description": "The client was successfully created"},
        400: {"description": "Error creating the client"},
        403: {"description": "The user is already bound to a customer"},
    },
)
async def create_customer(
    data: CustomerModelCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    if await Customer.get_by(owner_id=current_user.id, session=session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can create only 1 customer",
        )

    if customer := await customer_service.create_customer_with_admin_and_member(
        current_user=current_user,
        name=data.name,
        session=session,
    ):
        return CustomerModel.model_validate(customer, from_attributes=True)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not created")


@router.get(
    "/{customer_id}/admin",
    summary="Get customer admin",
)
async def get_customer_admin(
    customer_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    admin_ids = await customer_service.get_admins_by_customer(
        current_user=current_user,
        customer_id=customer_id,
        session=session,
    )
    if admin_ids is not False:
        return [
            UserModel.model_validate(
                user,
                from_attributes=True,
            )
            for user in await User.get_by_id_list(
                admin_ids,
                session=session,
            )
        ]
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


@router.patch(
    "/{customer_id}/admin",
    summary="Add customer admin",
)
async def patch_customer_admin(
    customer_id: uuid.UUID,
    admin_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    if await customer_service.add_admin(
        current_user=current_user,
        customer_id=customer_id,
        session=session,
        admin_id=admin_id,
    ):
        return True
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not added")


@router.delete(
    "/{customer_id}/admin",
    summary="Delete customer admin",
)
async def delete_customer_admin(
    customer_id: uuid.UUID,
    admin_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    if await customer_service.del_admin(
        current_user=current_user,
        customer_id=customer_id,
        admin_id=admin_id,
        session=session,
    ):
        return True
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not added")
