from typing import TYPE_CHECKING, Sequence

from core.schemas import OrderItemBaseS

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from core.models import Order
    from core.schemas import OrderBaseS, OrderItemBaseS

from core.repositories import OrderRepository, ProductRepository
from core.exceptions import OrderNotFoundError


class OrderService:
    _order_repository = OrderRepository
    _product_repository = ProductRepository

    @classmethod
    async def get_all(cls, session: "AsyncSession") -> Sequence["Order"]:
        return await cls._order_repository.get_all(session)

    @classmethod
    async def get_by_id(cls, session: "AsyncSession", order_id: int) -> "Order":
        order = await cls._order_repository.get_by_id(session, order_id)
        if order is None:
            raise OrderNotFoundError(f"Заказ с ID: {order_id} не найден.")
        return order

    @classmethod
    async def get_info(cls, session: "AsyncSession", order_id: int) -> "Order":
        order_info = await cls._order_repository.get_info(session, order_id)
        if order_info is None:
            raise OrderNotFoundError(f"Заказ с ID: {order_id} не найден.")
        return order_info

    @classmethod
    async def create(
        cls,
        session: "AsyncSession",
        items_data: Sequence["OrderItemBaseS"],
    ) -> "Order":
        items = [item.model_dump() for item in items_data]
        return await cls._order_repository.create(session, items)

    @classmethod
    async def update(
        cls,
        session: "AsyncSession",
        order: "Order",
        changes: "OrderBaseS",
    ) -> "Order":
        modified_order = await cls._order_repository.update(
            session, order, changes, partial=True
        )
        return modified_order
