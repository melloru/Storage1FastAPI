from typing import Annotated

from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.exceptions import NotEnoughProductInStock
from core.models import Order, Product, OrderItem
from core.repositories.base import BaseRepository, T


class OrderRepository(BaseRepository[Order]):
    model = Order

    async def create(self, products: list[(Product, int)]) -> Order:
        order = Order()
        for product_data in products:
            product, quantity = product_data
            await self.add_product_to_order(order, product, quantity)
        try:
            self.session.add(order)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Failed to create order due to integrity error.")
        return order

    async def add_product_to_order(self, order: Order, product: Product, quantity: int):
        if product.quantity_in_storage < quantity:
            raise NotEnoughProductInStock(
                f"Not enough stock for product {product.name}. "
                f"Available: {product.quantity_in_storage}, Requested: {quantity}."
            )

        order_item = OrderItem(order=order, product=product, quantity_in_order=quantity)
        order.products_details.append(order_item)

        product.quantity_in_storage -= quantity

    # async def create(self, products: list[(Product, int)]) -> Order:
    #     order = Order()
    #     for product_data in products:
    #         product, quantity = product_data
    #         await self.add_product_to_order(order, product, quantity)
    #     try:
    #         self.session.add(order)
    #         await self.session.commit()
    #     except IntegrityError:
    #         await self.session.rollback()
    #         raise ValueError("Failed to create order due to integrity error.")
    #     return order
    #
    # async def add_product_to_order(self, order: Order, product: Product, quantity: int):
    #     if product.quantity_in_storage < quantity:
    #         raise NotEnoughProductInStock(
    #             f"Not enough stock for product {product.name}. "
    #             f"Available: {product.quantity_in_storage}, Requested: {quantity}."
    #         )
    #
    #     order_item = OrderItem(order=order, product=product, quantity_in_order=quantity)
    #     order.products_details.append(order_item)
    #
    #     product.quantity_in_storage -= quantity


def get_order_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> OrderRepository:
    return OrderRepository(session)
