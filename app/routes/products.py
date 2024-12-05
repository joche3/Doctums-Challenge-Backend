from fastapi import APIRouter
from app.services.products import get_products, add_product

router = APIRouter()

@router.get("/products")
def get_products_route():
    return get_products()

@router.post("/products")
def add_product_route(product: dict):
    return add_product(product)