from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status

from core.schemas.order import OrderItemCreateS
from core.services import OrderService, get_order_service
from core.schemas import OrderBaseS

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get("/", response_model=Sequence[OrderBaseS])
async def get_all(service: Annotated["OrderService", Depends(get_order_service)]):
    return await service.get_all()


@router.post("/", response_model=OrderBaseS)
async def create(
    order: OrderItemCreateS,
    service: Annotated["OrderService", Depends(get_order_service)],
):
    try:
        return await service.create(order)
    except ValueError as e:
        if "Not enough stock" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{id}")
async def get_info():
    pass


@router.patch("/{id}/status")
async def update_status():
    pass
