from typing import Annotated

from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import Product
from core.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    model = Product


def get_product_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
) -> ProductRepository:
    return ProductRepository(session)
