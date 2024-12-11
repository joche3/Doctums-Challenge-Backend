from fastapi import APIRouter, Body
from app.services.projects import get_projects, add_project, update_project_acquired, buy_project

router = APIRouter()

@router.get("/projects")
def get_projects_route():
    return get_projects()

@router.post("/projects")
def add_project_route(project: dict):
    return add_project(project)

@router.put("/projects/{id}")
def update_project_acquired_route(id: int, acquired: bool = Body(...)):
    return update_project_acquired(id, acquired)

@router.post("/projects/{id}/buy")
def buy_project_route(id: int):
    return buy_project(id)