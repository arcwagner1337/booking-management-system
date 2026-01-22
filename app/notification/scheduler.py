from datetime import datetime, timedelta
import logging
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
)
from app.notification.factory import NotificationFactory

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """Шедулер для отправки уведомлений."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.batch_size = 50
        self.check_interval = 60

    async def get_pending_notifications(self) -> list[Notification]:
        """Получает уведомления, готовые к отправке."""
        now = datetime.now(ZoneInfo("UTC"))
        stmt = (
            sa.select(Notification)
            .where(
                and_(
                    Notification.status == NotificationStatus.PENDING,
                    Notification.scheduled_at <= now,
                    Notification.scheduled_at >= now - timedelta(hours=24),
                ),
            )
            .limit(self.batch_size)
        )

        result = await self.session.scalars(stmt)
        return result.all()

    async def process_notification(self, notification: Notification):
        # Меняем статус на "в обработке"
        notification.status = NotificationStatus.PROCESSING
        await self.session.commit()

        # Получаем данные бронирования
        booking = notification.booking

        # Формируем сообщение
        message = NotificationFactory.create_message(notification.type, booking)

        # Отправляем сообщение
        await self.send_telegram_message(
            user_id=notification.user_id,
            message=message,
        )

        # Обновляем статус
        notification.status = NotificationStatus.SENT
