from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.depends import provider

convention = {
    "all_column_names": lambda constraint, table: "_".join(  # noqa: ARG005
        [column.name for column in constraint.columns.values()],
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    _primary_key_name = "id"

    metadata = sa.MetaData(naming_convention=convention)

    @classmethod
    @provider.inject_session
    async def get(cls, id: int, session: AsyncSession = None):  # noqa: A002
        """Get one record by primary key"""
        stmt = sa.select(cls).where(getattr(cls, cls._primary_key_name) == id)
        return await session.scalar(stmt)

    @classmethod
    @provider.inject_session
    async def get_by_id_list(
        cls,
        id_list: list[int],
        session: AsyncSession = None,
    ) -> list[any]:
        """Get multiple records by primary key list"""
        stmt = sa.select(cls).where(
            getattr(cls, cls._primary_key_name).in_(id_list),
        )
        result = await session.scalars(stmt)
        return result.all()

    @classmethod
    @provider.inject_session
    async def get_all(cls, session: AsyncSession = None):
        """Get all records"""
        stmt = sa.select(cls)
        return await session.scalars(stmt)

    @classmethod
    @provider.inject_session
    async def get_all_by(cls, session: AsyncSession = None, **kwargs):
        """Get all records based on the conditions"""
        conditions = [getattr(cls, k) == v for k, v in kwargs.items()]
        stmt = sa.select(cls).where(sa.and_(*conditions))
        return await session.scalars(stmt)

    @classmethod
    @provider.inject_session
    async def get_by(cls, session: AsyncSession = None, **kwargs):
        """Get one record based on the conditions"""
        conditions = [getattr(cls, k) == v for k, v in kwargs.items()]
        stmt = sa.select(cls).where(sa.and_(*conditions))
        return await session.scalar(stmt)

    @classmethod
    @provider.inject_session
    async def create(cls, session: AsyncSession = None, **kwargs):
        """Create a record with the return of the created object"""
        stmt = pg_insert(cls).values(kwargs).returning(cls)
        return await session.scalar(stmt)

    @classmethod
    @provider.inject_session
    async def update(
        cls,
        id: int,  # noqa: A002
        session: AsyncSession = None,
        **kwargs,
    ):
        """Updating a record with the return of the updated object"""
        stmt = (
            sa.update(cls)
            .where(getattr(cls, cls._primary_key_name) == id)
            .values(kwargs)
            .returning(cls)
        )
        return await session.scalar(stmt)

    @classmethod
    @provider.inject_session
    async def update_or_create(
        cls,
        id: str | int,  # noqa: A002
        session: AsyncSession = None,
        **kwargs,
    ):
        """Update or create a record with one UPSERT query"""
        kwargs[cls._primary_key_name] = id
        stmt = (
            pg_insert(cls)
            .values(kwargs)
            .on_conflict_do_update(index_elements=[cls._primary_key_name], set_=kwargs)
            .returning(cls)
        )
        return await session.scalar(stmt)

    @classmethod
    @provider.inject_session
    async def delete(cls, id: str | int, session: AsyncSession = None) -> None:  # noqa: A002
        """Delete a record"""
        stmt = sa.delete(cls).where(getattr(cls, cls._primary_key_name) == id)
        await session.provider.inject_session(stmt)

    def to_dict(self) -> dict[str, any]:
        """Convert object to dictionary"""
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class CreatedMixin:
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        server_default=sa.func.now(),
    )


class UpdatedMixin:
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )


class BaseWithDt(Base, CreatedMixin, UpdatedMixin):
    """Basic model with timestamps"""

    __abstract__ = True


table = Base.metadata
