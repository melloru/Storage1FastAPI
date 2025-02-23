from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin


if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(Base, IdIntPkMixin):
    __tablename__ = "orderitems"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity_in_order: Mapped[int] = mapped_column(default=1, server_default="1")

    order: Mapped["Order"] = relationship("Order", back_populates="products_details")
    product: Mapped["Product"] = relationship(
        "Product", back_populates="orders_details"
    )
