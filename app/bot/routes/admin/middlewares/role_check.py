from collections.abc import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services.user.user import user_service
from app.infrastructure.database.models import (
    Customer,
    CustomerAdmin,
)


class RoleCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict,
    ):
        session: AsyncSession = data.get("session")
        if not session:
            await self._deny_access(event, "⛔ Ошибка доступа к базе данных")
            return None

        tg_user = event.from_user
        if not tg_user:
            await self._deny_access(event, "⛔ Пользователь не найден")
            return None

        try:
            user = await user_service.update_user_from_tlg(
                tlg_user=tg_user,
                bot_id=event.bot.id,
                session=session,
            )
        except Exception:
            await self._deny_access(event, "⛔ У вас нет доступа")
            return None

        if not user:
            await self._deny_access(event, "⛔ У вас нет доступа")
            return None

        owner_result = await session.execute(
            select(Customer.id).where(Customer.owner_id == user.id),
        )
        owner_customer_ids = [row[0] for row in owner_result.all()]

        admin_result = await session.execute(
            select(CustomerAdmin.customer_id).where(
                CustomerAdmin.user_id == user.id,
            ),
        )
        admin_customer_ids = [row[0] for row in admin_result.all()]

        if not owner_customer_ids and not admin_customer_ids:
            await self._deny_access(event, "⛔ У вас нет доступа")
            return None

        data["user"] = user
        data["role"] = "owner" if owner_customer_ids else "admin"
        data["customer_ids"] = set(owner_customer_ids + admin_customer_ids)

        return await handler(event, data)

    async def _deny_access(
        self,
        event: Message | CallbackQuery,
        message: str,
    ):
        try:
            if isinstance(event, CallbackQuery):
                await event.answer(message, show_alert=True)
            elif isinstance(event, Message):
                await event.answer(message)
        except Exception:
            pass
