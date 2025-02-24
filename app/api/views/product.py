from typing import Annotated, Sequence, TYPE_CHECKING

from fastapi import APIRouter, Depends

from core.schemas import (
    ProductCreateS,
    ProductS,
    ProductUpdatePartialS,
    ProductUpdateS,
)

from core.services import ProductService, get_product_service

from api.dependencies.product import get_product_by_id


if TYPE_CHECKING:
    from core.models import Product

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=Sequence[ProductS])
async def get_all(
    service: Annotated["ProductService", Depends(get_product_service)],
):
    return await service.get_all()


@router.get("/{id}", response_model=ProductS)
async def get_by_id(
    product: Annotated[ProductS, Depends(get_product_by_id)],
):
    return product


@router.post("/", response_model=ProductCreateS)
async def create(
    product: ProductCreateS,
    service: Annotated["ProductService", Depends(get_product_service)],
):
    return await service.create(product)


@router.put("/{id}", response_model=ProductS)
async def update(
    product: Annotated["Product", Depends(get_product_by_id)],
    updated_product: ProductUpdateS,
    service: Annotated["ProductService", Depends(get_product_service)],
):
    return await service.update(product, updated_product)


@router.patch("/{id}", response_model=ProductS)
async def update_partial(
    product: Annotated["Product", Depends(get_product_by_id)],
    updated_product: ProductUpdatePartialS,
    service: Annotated["ProductService", Depends(get_product_service)],
):
    return await service.update_partial(product, updated_product)


@router.delete("/{id}", response_model=None)
async def delete(
    product: Annotated["Product", Depends(get_product_by_id)],
    service: Annotated["ProductService", Depends(get_product_service)],
):
    await service.delete(product)
