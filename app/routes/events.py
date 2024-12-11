from fastapi import APIRouter, Body
from app.services.events import get_events, add_event, update_event, delete_event

router = APIRouter()

@router.get("/events")
def get_events_route():
    return get_events()

@router.post("/events")
def add_event_route(event: dict):
    return add_event(event)

@router.put("/events/{id}")
def update_event_route(id: int, updated_event: dict = Body(...)):
    return update_event(id, updated_event)

@router.delete("/events/{id}")
def delete_event_route(id: int):
    return delete_event(id)