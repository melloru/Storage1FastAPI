from sqlalchemy.orm import Mapped

from .base import Base
from .mixins import IdIntPkMixin


class Product(Base, IdIntPkMixin):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity_in_storage: Mapped[int]
