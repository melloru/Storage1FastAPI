from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order_item import OrderItem

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin


class Product(Base, IdIntPkMixin):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[int]
    quantity_in_storage: Mapped[int]

    # Возвращает все заказы, связанные с продуктом
    orders_details: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
    )
