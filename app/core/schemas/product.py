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
