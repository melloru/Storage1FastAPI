from fastapi import APIRouter

from .views.product import router as product_router
from .views.order import router as order_router

router = APIRouter()

router.include_router(product_router)
router.include_router(order_router)
