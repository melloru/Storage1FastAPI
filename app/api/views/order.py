from typing import TYPE_CHECKING, Annotated, Sequence, Dict

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import Order

from fastapi import APIRouter, Depends, HTTPException, Path, status

from core import db_helper
from core.services import OrderService
from core.schemas import (
    OrderS,
    OrderBaseS,
    OrderCreateS,
    OrderInfoS,
    OrderItemBaseS,
    OrderUpdateS,
)
from core.exceptions import (
    NotEnoughProductInStockError,
    ProductNotFoundError,
    OrderNotFoundError,
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


async def get_order_or_404(
    order_id: Annotated[int, Path],
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> "Order":
    try:
        return await OrderService.get_by_id(session, order_id)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=Sequence[OrderS])
async def get_all(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):  # Переделать
    return await OrderService.get_all(session)


@router.get("/{id}", response_model=OrderInfoS)
async def get_info(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    order_id: int,
):
    try:
        return await OrderService.get_info(session, order_id)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=OrderCreateS)
async def create(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    order_items: Sequence[OrderItemBaseS],
):
    try:
        return await OrderService.create(session, order_items)
    except NotEnoughProductInStockError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch("/{id}/status", response_model=OrderUpdateS)
async def update_status(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    order: Annotated["Order", Depends(get_order_or_404)],
    changes: OrderBaseS,
):
    return await OrderService.update(session, order, changes)
