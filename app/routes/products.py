from fastapi import APIRouter, Body
from app.services.products import get_products, add_product, update_product_acquired, buy_product

router = APIRouter()

@router.get("/products")
def get_products_route():
    return get_products()

@router.post("/products")
def add_product_route(product: dict):
    return add_product(product)

@router.put("/products/{id}")
def update_product_acquired_route(id: int, acquired: bool = Body(...)):
    return update_product_acquired(id, acquired)

@router.post("/products/{id}/buy")
def buy_product_route(id: int):
    return buy_product(id)