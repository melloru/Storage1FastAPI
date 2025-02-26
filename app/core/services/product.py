from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.models import Product
    from core.schemas import ProductCreateS, ProductUpdatePartialS, ProductUpdateS

from sqlalchemy.exc import IntegrityError

from core.repositories import ProductRepository
from core.exceptions import (
    ProductNotFoundError,
    ProductAlreadyExistsError,
    ProductInOrderError,
)


class ProductService:
    _product_repository = ProductRepository

    @classmethod
    async def get_all(cls, session: "AsyncSession") -> Sequence["Product"]:
        return await cls._product_repository.get_all(session)

    @classmethod
    async def get_by_id(cls, session: "AsyncSession", product_id: int) -> "Product":
        product = await cls._product_repository.get_by_id(session, product_id)
        if product is None:
            raise ProductNotFoundError(f"Товар с ID: {product_id} не найден.")
        return product

    @classmethod
    async def create(
        cls, session: "AsyncSession", product: "ProductCreateS"
    ) -> "Product":
        try:
            return await cls._product_repository.create(session, product)
        except IntegrityError:
            raise ProductAlreadyExistsError(
                f"Товар с именем: '{product.name}' уже существует."
            )

    @classmethod
    async def delete(cls, session: "AsyncSession", product: "Product"):
        try:
            await cls._product_repository.delete(session, product)
        except IntegrityError:  # Переделать
            raise ProductInOrderError(f"Продукт есть в каком-то заказе.")

    @classmethod
    async def update(
        cls,
        session: "AsyncSession",
        product: "Product",
        changes: "ProductUpdateS",
    ) -> "Product":
        try:
            return await cls._product_repository.update(session, product, changes)
        except IntegrityError:
            raise ProductAlreadyExistsError(
                f"Товар с именем: '{changes.name}' уже существует."
            )

    @classmethod
    async def update_partial(
        cls,
        session: "AsyncSession",
        product: "Product",
        changes: "ProductUpdatePartialS",
    ) -> "Product":
        modified_product = await cls._product_repository.update(
            session, product, changes, partial=True
        )
        return modified_product
