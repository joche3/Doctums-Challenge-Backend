from fastapi import APIRouter, Body
from app.services.resources import get_resources, add_resource, update_resource_acquired, buy_resource

router = APIRouter()

@router.get("/resources")
def get_resources_route():
    return get_resources()

@router.post("/resources")
def add_resource_route(resource: dict):
    return add_resource(resource)

@router.put("/resources/{id}")
def update_resource_acquired_route(id: int, acquired: bool = Body(...)):
    return update_resource_acquired(id, acquired)

@router.post("/resources/{id}/buy")
def buy_resource_route(id: int):
    return buy_resource(id)