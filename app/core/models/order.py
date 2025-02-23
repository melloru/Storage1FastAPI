from enum import Enum
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import IdIntPkMixin


if TYPE_CHECKING:
    from .order_item import OrderItem


class OrderStatus(Enum):
    IN_PROGRESS = "in progress"
    SENT = "sent"
    DELIVERED = "delivered"


class Order(Base, IdIntPkMixin):
    __tablename__ = "orders"

    status: Mapped[OrderStatus] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow(),
    )

    # Возвращает все продукты, связанные с заказом
    products_details: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
    )
