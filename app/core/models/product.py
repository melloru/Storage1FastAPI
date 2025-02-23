from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins import IdIntPkMixin


if TYPE_CHECKING:
    from .order_item import OrderItem


class Product(Base, IdIntPkMixin):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity_in_storage: Mapped[int]

    # Возвращает все заказы, связанные с продуктом
    orders_details: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
