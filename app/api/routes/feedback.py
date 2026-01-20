from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, conint
import sqlalchemy as sa

from app.depends import AsyncSession, provider
from app.infrastructure.database.models.feedback import Feedback


class FeedbackCreate(BaseModel):
    booking_id: int = Field(..., example=1)
    rating: conint(ge=1, le=5) = Field(..., example=5)
    comment: str | None = Field(None, example="Всё понравилось!")


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    data: FeedbackCreate,
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Создание отзыва (feedback) после бронирования
    """

    feedback = Feedback(
        booking_id=data.booking_id,
        rating=data.rating,
        comment=data.comment,
        # user_id и customer_id обычно берутся из токена,
        # здесь для примера можно захардкодить или получить из Depends
        user_id=session.info.get("user_id"),
        customer_id=session.info.get("customer_id"),
    )

    session.add(feedback)

    try:
        await session.commit()
    except sa.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid booking or user",
        ) from None

    return {"status": "ok"}
