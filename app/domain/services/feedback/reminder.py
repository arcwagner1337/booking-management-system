from datetime import datetime, timedelta, timezone

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.booking import Booking


async def send_review_reminders(session: AsyncSession):
    cutoff_time = datetime.now(tz=timezone.utc) - timedelta(minutes=15)

    stmt = (
        sa.select(Booking).where(Booking.end_time <= cutoff_time)
        # TODO: Добавить в таблицу Booking поле feedback_sent которое отражает состояние отправлена ли заявка на отзыв или еще нет # noqa: E501, TD002, TD003
        # .where(Booking.feedback_sent.is_(False))
    )

    bookings = (await session.scalars(stmt)).all()

    for booking in bookings:
        # TODO: отправка сообщения (telegram / email)  # noqa: TD002, TD003
        print(  # noqa: T201
            f"Send feedback request for booking {booking.id}",
        )

        booking.feedback_sent = True

    await session.commit()
