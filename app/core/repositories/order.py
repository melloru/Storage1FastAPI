from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models import Order, Product, OrderItem
from core.schemas import OrderBaseS
from core.repositories import BaseRepository
from core.exceptions import NotEnoughProductInStockError, ProductNotFoundError


class OrderRepository(BaseRepository[Order]):
    _model = Order

    @classmethod
    async def get_all(
        cls,
        session: "AsyncSession",
    ) -> Sequence[Order]:
        return await super().get_all(session)

    @classmethod
    async def update(
        cls,
        session: "AsyncSession",
        order: Order,
        changes_order: OrderBaseS,
        partial: bool = False,
    ) -> Order:
        return await super().update(session, order, changes_order)

    @classmethod
    async def create(
        cls,
        session: "AsyncSession",
        items_data: list[dict],
    ) -> Order:
        async with session.begin():
            order = cls._model()
            order.products_details = [OrderItem(**item) for item in items_data]
            for item in order.products_details:

                stmt = select(Product).filter(Product.id == item.product_id)
                result = await session.execute(stmt)
                product = result.scalar_one_or_none()

                if product is None:
                    raise ProductNotFoundError(
                        f"Товар с ID: {item.product_id} не найден."
                    )
                elif product.quantity_in_storage < item.quantity:
                    raise NotEnoughProductInStockError(
                        f"Недостаточно товара: '{product.name}'. "
                        f"Доступно: {product.quantity_in_storage}, Запрошено: {item.quantity}."
                    )

                product.quantity_in_storage -= item.quantity

            session.add(order)

        return order

    @classmethod
    async def get_info(
        cls,
        session: "AsyncSession",
        order_id: int,
    ) -> Order | None:
        stmt = (
            select(Order)
            .filter_by(id=order_id)
            .options(
                selectinload(Order.products_details).joinedload(OrderItem.product),
            )
            .order_by(Order.id)
        )
        order = await session.execute(stmt)

        return order.scalar_one_or_none()

    @classmethod
    async def add_product_to_order(
        cls,
        order: Order,
        product: Product,
        quantity: int,
    ):
        if product.quantity_in_storage < quantity:
            raise NotEnoughProductInStockError(
                f"Not enough stock for product {product.name}. "
                f"Available: {product.quantity_in_storage}, Requested: {quantity}."
            )

        order_item = OrderItem(order=order, product=product, quantity_in_order=quantity)
        order.products_details.append(order_item)

        product.quantity_in_storage -= quantity
