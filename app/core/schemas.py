import datetime

from typing import List, Sequence

from pydantic import BaseModel


class ProductBaseS(BaseModel):
    name: str
    description: str
    price: int
    quantity_in_storage: int


class ProductS(ProductBaseS):
    id: int


class ProductCreateS(ProductBaseS):
    pass


class ProductUpdateS(ProductCreateS):
    pass


class ProductUpdatePartialS(ProductCreateS):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity_in_storage: int | None = None


class OrderBaseS(BaseModel):
    status: str


class OrderS(OrderBaseS):
    id: int
    created_at: datetime.datetime


class OrderUpdateS(OrderBaseS):
    pass


class OrderItemBaseS(BaseModel):
    product_id: int
    quantity: int


class OrderCreateS(OrderBaseS):
    products_details: Sequence[OrderItemBaseS]


class OrderInfoS(OrderBaseS):
    created_at: datetime.datetime
    products_details: Sequence[OrderItemBaseS]
