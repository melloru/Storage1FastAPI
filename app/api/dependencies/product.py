from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException, Path, status

from core.models import Product
from core.services import ProductService, get_product_service


async def get_product_by_id(
    service: Annotated["ProductService", Depends(get_product_service)],
    product_id: Annotated[int, Path],
) -> Product:
    product = await service.get_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с ID: {product_id} не найден!",
        )

    return product
