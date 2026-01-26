from datetime import datetime
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.infrastructure.database.models.notification import (
    Notification,
    NotificationStatus,
)


class NotificationService:
    """Сервис для управления уведомлениями."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pending_notifications(self) -> list[Notification]:
        """Получает уведомления, готовые к отправке."""
        now = datetime.now(ZoneInfo("UTC"))
        query = select(Notification).where(
            sa.and_(
                Notification.status == NotificationStatus.PENDING,
                Notification.scheduled_at <= now,
            ),
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def mark_as_sent(
        self,
        notification: Notification,
        message: str,
    ) -> None:
        """Помечает уведомление как отправленное."""
        notification.status = NotificationStatus.SENT
        notification.processed_at = datetime.now(ZoneInfo("UTC"))
        notification.message = message
        await self.session.commit()

    async def mark_as_failed(
        self,
        notification: Notification,
        error: str,
    ) -> None:
        """Помечает уведомление как неудачное."""
        notification.status = NotificationStatus.FAILED
        notification.processed_at = datetime.now(ZoneInfo("UTC"))
        notification.error = error
        await self.session.commit()
