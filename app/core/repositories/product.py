from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas import ProductBaseS
from core.repositories import BaseRepository


class ProductRepository(BaseRepository[Product]):
    _model = Product

    @classmethod
    async def get_all(
        cls,
        session: "AsyncSession",
    ) -> Sequence[Product]:
        return await super().get_all(session)

    @classmethod
    async def get_by_id(
        cls,
        session: "AsyncSession",
        product_id: int,
    ) -> Product:
        return await super().get_by_id(session, product_id)

    @classmethod
    async def update(
        cls,
        session: "AsyncSession",
        product: Product,
        changes: ProductBaseS,
        partial: bool = False,
    ) -> Product:
        return await super().update(session, product, changes)

    @classmethod
    async def create(
        cls,
        session: "AsyncSession",
        product: ProductBaseS,
    ) -> Product:
        return await super().create(session, product)
