from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IdIntPkMixin


class OrderItem(Base, IdIntPkMixin):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity_in_order: Mapped[int] = mapped_column(default=1, server_default="1")
