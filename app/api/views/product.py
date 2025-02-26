from typing import TYPE_CHECKING, Annotated, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import Product

from fastapi import APIRouter, Depends, HTTPException, Path, status

from core import db_helper
from core.services import ProductService
from core.schemas import (
    ProductCreateS,
    ProductS,
    ProductUpdatePartialS,
    ProductUpdateS,
)
from core.exceptions import (
    ProductNotFoundError,
    ProductAlreadyExistsError,
    ProductInOrderError,
)


router = APIRouter(prefix="/products", tags=["Products"])


async def get_product_or_404(
    product_id: Annotated[int, Path],
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> "Product":
    try:
        return await ProductService.get_by_id(session, product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=Sequence[ProductS])
async def get_all(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    return await ProductService.get_all(session)


@router.get("/{id}", response_model=ProductS)
async def get_by_id(
    product: Annotated["Product", Depends(get_product_or_404)],
):
    return product


@router.post("/", response_model=ProductCreateS)
async def create(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    product: ProductCreateS,
):
    try:
        return await ProductService.create(session, product)
    except ProductAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=ProductS)
async def update(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    product: Annotated["Product", Depends(get_product_or_404)],
    changes: ProductUpdateS,
):
    try:
        return await ProductService.update(session, product, changes)
    except ProductAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{id}", response_model=ProductS)
async def update_partial(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    product: Annotated["Product", Depends(get_product_or_404)],
    changes: ProductUpdatePartialS,
):
    return await ProductService.update_partial(session, product, changes)


@router.delete("/{id}", response_model=None)
async def delete(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    product: Annotated["Product", Depends(get_product_or_404)],
):  # Переделать
    try:
        await ProductService.delete(session, product)
    except ProductInOrderError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
