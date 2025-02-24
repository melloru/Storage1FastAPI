from typing import Sequence, Annotated

from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError

from core.exceptions import NotEnoughProductInStock
from core.repositories import OrderRepository, BaseRepository, ProductRepository
from core.repositories.order import get_order_repository
from core.repositories.product import get_product_repository
from core.models import Order, OrderItem, Product
from core.schemas.order import OrderItemCreateS
from core.uow import unit_of_work


class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        product_repository: ProductRepository,
    ):
        self.repository = repository
        self.product_repository = product_repository

    async def get_all(self) -> Sequence[Order]:
        return await self.repository.get_all()

    async def create(self, order_items: OrderItemCreateS):
        with unit_of_work() as uow:
            self.product_repository.session = uow.session
            cart_products = [
                (
                    await self.product_repository.get_by_id(product.product_id),
                    product.quantity,
                )
                for product in order_items.products_details
            ]

            new_order = await self.repository.create(cart_products)
            return new_order

    async def add_product_to_order(self, order: Order, product: Product, quantity: int):
        if product.quantity_in_storage < quantity:
            raise NotEnoughProductInStock(
                f"Not enough stock for product {product.name}. "
                f"Available: {product.quantity_in_storage}, Requested: {quantity}."
            )

        order_item = OrderItem(order=order, product=product, quantity_in_order=quantity)
        order.products_details.append(order_item)

        product.quantity_in_storage -= quantity

    # async def create(self, order_items: OrderItemCreateS):
    #     cart_products = [
    #         (
    #             await self.product_repository.get_by_id(product.product_id),
    #             product.quantity,
    #         )
    #         for product in order_items.products_details
    #     ]
    #
    #     new_order = await self.repository.create(cart_products)
    #     return new_order

    # async def create(self, order_items: OrderItemCreateS):
    #     new_order = Order()
    #
    #     for cart_product in order_items.products_details:
    #         product = await self.product_repository.get_by_id(cart_product.product_id)
    #         await self.add_product_to_order(new_order, product, cart_product.quantity)
    #     try:
    #         await self.repository.create(new_order)
    #     except IntegrityError:
    #         raise ValueError("Failed to create order due to integrity error.")
    #
    #     return new_order

    # async def check_quantity(self, product_id: int, quantity: int) -> bool:
    #     product = await self.product_repository.get_product(product_id)
    #     return product.stock >= quantity

    async def add_product_to_order(self, order: Order, product: Product, quantity: int):
        if product.quantity_in_storage < quantity:
            raise IntegrityError(
                f"Not enough stock for product {product.name}. "
                f"Available: {product.quantity_in_storage}, Requested: {quantity}."
            )
        order_item = OrderItem(order=order, product=product, quantity_in_order=quantity)
        order.products_details.append(order_item)

        product.quantity_in_storage -= quantity


def get_order_service(
    repository: Annotated["OrderRepository", Depends(get_order_repository)],
    product_repository: Annotated["ProductRepository", Depends(get_product_repository)],
) -> OrderService:
    return OrderService(
        repository=repository,
        product_repository=product_repository,
    )
