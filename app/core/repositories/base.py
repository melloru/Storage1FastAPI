from typing import TYPE_CHECKING, TypeVar, Generic, Sequence, Type

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.models import Base


T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    _model: Type[T]

    @classmethod
    async def get_all(
        cls,
        session: "AsyncSession",
    ) -> Sequence[T]:
        stmt = select(cls._model)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_by_id(
        cls,
        session: "AsyncSession",
        data_id: int,
    ) -> T | None:
        stmt = select(cls._model).filter_by(id=data_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        session: "AsyncSession",
        exemplar: BaseModel,
    ) -> T:
        new_exemplar = cls._model(**exemplar.model_dump())
        session.add(new_exemplar)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_exemplar

    @classmethod
    async def update(
        cls,
        session: "AsyncSession",
        exemplar: T,
        changes: BaseModel,
        partial: bool = False,
    ) -> T:
        for name, value in changes.model_dump(exclude_unset=partial).items():
            if value is not None:
                setattr(exemplar, name, value)
        await session.commit()
        return exemplar

    @classmethod
    async def delete(
        cls,
        session: "AsyncSession",
        exemplar: T,
    ) -> None:
        await session.delete(exemplar)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
