from fastapi import APIRouter, Body
from app.services.efficiencies import get_efficiencies, add_efficiency, update_efficiency_points

router = APIRouter()

@router.get("/efficiencies")
def get_efficiencies_route():
    return get_efficiencies()

@router.post("/efficiencies")
def add_efficiency_route(efficiency: dict):
    return add_efficiency(efficiency)

# Ruta para actualizar los puntos de una eficiencia
@router.put("/efficiencies/{id}")  # Asegúrate de que la ruta sea "/efficiencies/{id}"
def update_efficiency_points_route(id: int, points: int = Body(...)):
    return update_efficiency_points(id, points)