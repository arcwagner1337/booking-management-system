from uuid import UUID

import sqlalchemy as sa

from app.config import config
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.users import (
    Customer,
    CustomerAdmin,
    CustomerMember,
    User,
)


class CustomerService:
    @provider.inject_session
    async def create_customer_with_admin_and_member(
        self,
        current_user: User,
        name: str,
        session: AsyncSession | None = None,
        **kwargs,
    ) -> Customer:
        customer = await Customer.create(
            owner_id=current_user.id,
            session=session,
            name=name,
            **kwargs,
        )
        if customer:
            await CustomerAdmin.create(
                user_id=current_user.id,
                customer_id=customer.id,
                session=session,
            )
            await CustomerMember.create(
                user_id=current_user.id,
                customer_id=customer.id,
                session=session,
            )
            await session.commit()
            if config.bot.TEST_BOT_TOKEN:
                from app.bot import bot_manager  # noqa: PLC0415

                await bot_manager.add_bot(
                    bot_token=config.bot.TEST_BOT_TOKEN,
                    owner_id=customer.id,
                )

            return customer
        return None

    @provider.inject_session
    async def check_customer_owner(
        self,
        current_user: User,
        customer_id: UUID,
        session: AsyncSession | None = None,
    ) -> Customer | None:
        customer = await Customer.get_by(
            id=customer_id,
            owner_id=current_user.id,
            session=session,
        )
        if not customer:
            return None
        if not (
            current_user.id == customer.owner_id
            or (
                await CustomerAdmin.get_by(
                    session=session,
                    user_id=current_user.id,
                    customer_id=customer.id,
                )
            )
        ):
            return None
        return customer

    @provider.inject_session
    async def add_admin(
        self,
        current_user: User,
        customer_id: UUID,
        admin_id: UUID,
        session: AsyncSession | None = None,
    ):
        customer = await self.check_customer_owner(
            current_user=current_user,
            customer_id=customer_id,
            session=session,
        )
        if not customer:
            return False

        existing_admin = await CustomerAdmin.get_by(
            user_id=admin_id,
            customer_id=customer.id,
            session=session,
        )
        if not existing_admin:
            await CustomerAdmin.create(
                user_id=admin_id,
                customer_id=customer.id,
                session=session,
            )
        await session.commit()
        return True

    @provider.inject_session
    async def del_admin(
        self,
        current_user: User,
        customer_id: UUID,
        admin_id: UUID,
        session: AsyncSession | None = None,
    ):
        customer = await self.check_customer_owner(
            current_user=current_user,
            customer_id=customer_id,
            session=session,
        )
        if not customer:
            return False
        existing_admin = await CustomerAdmin.get_by(
            user_id=admin_id,
            customer_id=customer.id,
            session=session,
        )
        if existing_admin:
            stmt = sa.delete(CustomerAdmin).where(
                CustomerAdmin.user_id == admin_id,
                CustomerAdmin.customer_id == customer.id,
            )
            await session.execute(stmt)
            await session.commit()
            return True
        return False

    async def get_admins_by_customer(
        self,
        current_user: User,
        customer_id: UUID,
        session: AsyncSession | None = None,
    ) -> list[UUID]:
        customer = await self.check_customer_owner(
            current_user=current_user,
            customer_id=customer_id,
            session=session,
        )
        if not customer:
            return False
        admins = await CustomerAdmin.get_all_by(
            customer_id=customer_id,
            session=session,
        )

        return [a.user_id for a in admins]


customer_service = CustomerService()
