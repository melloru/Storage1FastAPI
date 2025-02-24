from typing import TYPE_CHECKING, Annotated, Sequence

from fastapi import Depends

from core.repositories.product import get_product_repository
from core.schemas import ProductCreateS, ProductUpdatePartialS, ProductS, ProductUpdateS
from core.models import Product

if TYPE_CHECKING:
    from core.repositories import ProductRepository


class ProductService:
    def __init__(self, repository: "ProductRepository"):
        self.repository = repository

    async def get_all(self) -> Sequence[Product]:
        return await self.repository.get_all()

    async def get_by_id(self, product_id: int) -> Product:
        return await self.repository.get_by_id(product_id)

    async def create(self, product: ProductCreateS) -> Product:
        return await self.repository.create(product)

    async def delete(self, product: Product):
        await self.repository.delete(exemplar=product)

    async def update(
        self,
        product: Product,
        updated_product: ProductUpdateS,
    ) -> Product:
        return await self.repository.update(
            exemplar=product,
            updated_exemplar=updated_product,
        )

    async def update_partial(
        self,
        product: Product,
        updated_product: ProductUpdatePartialS,
    ) -> Product:
        return await self.repository.update(
            exemplar=product,
            updated_exemplar=updated_product,
            partial=True,
        )


def get_product_service(
    repository: Annotated["ProductRepository", Depends(get_product_repository)],
) -> ProductService:
    return ProductService(repository=repository)
