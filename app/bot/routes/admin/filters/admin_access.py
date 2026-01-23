from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import (
    Customer,
    CustomerAdmin,
    User,
)


class AdminAccessFilter(BaseFilter):
    async def __call__(
        self,
        event: Message | CallbackQuery,
        session: AsyncSession,
    ) -> bool:
        tg_user = event.from_user
        if not tg_user:
            return False

        result = await session.execute(
            select(User).where(User.tlg_id == tg_user.id),
        )
        user: User | None = result.scalar_one_or_none()

        if not user:
            await self._deny(event)
            return False

        owner_customers = await session.execute(
            select(Customer.id).where(Customer.owner_id == user.id),
        )
        owner_customer_ids = [row[0] for row in owner_customers.all()]

        admin_customers = await session.execute(
            select(CustomerAdmin.customer_id).where(
                CustomerAdmin.user_id == user.id,
            ),
        )
        admin_customer_ids = [row[0] for row in admin_customers.all()]

        if not owner_customer_ids and not admin_customer_ids:
            await self._deny(event)
            return False

        event.user = user
        event.role = "owner" if owner_customer_ids else "admin"
        event.customer_ids = set(owner_customer_ids + admin_customer_ids)

        return True

    async def _deny(self, event: Message | CallbackQuery):
        text = "⛔ У вас нет доступа"

        if isinstance(event, CallbackQuery):
            await event.answer(text, show_alert=True)
        else:
            await event.answer(text)
