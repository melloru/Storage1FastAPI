from pydantic import BaseModel


class OrderBaseS(BaseModel):
    status: str


class OrderProductS(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreateS(BaseModel):
    products_details: list[OrderProductS]


# class ShoppingCartS(BaseModelS):
#     products: list[OrderProductS]


# class ProductS(ProductBaseS):
#     id: int
#
#
# class ProductCreateS(BaseCreateS):
#     pass
#
#
# class ProductUpdateS(BaseUpdateS):
#     name: str
#     description: str
#     price: int
#     quantity_in_storage: int
#
#
# class ProductUpdatePartialS(BaseUpdatePartialS):
#     name: str | None = None
#     description: str | None = None
#     price: int | None = None
#     quantity_in_storage: int | None = None
