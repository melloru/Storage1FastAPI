class OrderNotFoundError(Exception):
    pass


class NotEnoughProductInStockError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class ProductAlreadyExistsError(Exception):
    pass


class ProductInOrderError(Exception):
    pass
