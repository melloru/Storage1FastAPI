from typing import TypeVar, Generic, Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base
from pydantic import BaseModel

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: T

    def __init__(self, session: "AsyncSession"):
        self.session = session

    async def get_all(self) -> Sequence[T]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, data_id: int) -> T | None:
        stmt = select(self.model).filter_by(id=data_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, exemplar: BaseModel) -> T:
        new_exemplar = self.model(**exemplar.model_dump())
        self.session.add(new_exemplar)
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
        return new_exemplar

    async def update(
        self,
        exemplar: T,
        updated_exemplar: BaseModel,
        partial: bool = False,
    ) -> T:
        for name, value in updated_exemplar.model_dump(exclude_unset=partial).items():
            setattr(exemplar, name, value)
        await self.session.commit()
        return exemplar

    async def delete(self, exemplar: T) -> None:
        await self.session.delete(exemplar)
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def save(self):
        await self.session.commit()
