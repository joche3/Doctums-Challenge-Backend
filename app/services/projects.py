import json
import os
from app.services.player import load_player, save_player
from fastapi.responses import JSONResponse
from app.services.efficiencies import load_efficiencies, efficiencies_file_path

# Ruta del archivo JSON de proyectos
data_folder = os.path.join(os.path.dirname(__file__), "../data")
projects_file_path = os.path.join(data_folder, "proyectos.json")

# Cargar los proyectos desde el archivo JSON
def load_projects():
    with open(projects_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Obtener los proyectos
def get_projects():
    projects = load_projects()
    return {"projects": projects}

# Agregar un nuevo proyecto
def add_project(project: dict):
    projects = load_projects()
    new_id = max([p["id"] for p in projects]) + 1 if projects else 1
    project["id"] = new_id
    project["efficiency_points"] = project.get("efficiency_points", 0)  # Inicializado en 0 si no está presente
    project["acquired"] = project.get("acquired", False)  # Inicializado en False si no está presente
    projects.append(project)

    # Guardar el nuevo proyecto en el archivo JSON
    with open(projects_file_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=4, ensure_ascii=False)

    return {"message": "Project added successfully", "project": project}

# Actualizar el campo 'acquired' de un proyecto
def update_project_acquired(id: int, acquired: bool):
    projects = load_projects()

    # Buscar el proyecto por 'id'
    for project in projects:
        if project["id"] == id:
            project["acquired"] = acquired
            # Guardar los proyectos actualizados en el archivo JSON
            with open(projects_file_path, 'w', encoding='utf-8') as f:
                json.dump(projects, f, indent=4, ensure_ascii=False)
            return {"message": f"Project 'acquired' field updated for id {id}", "project": project}

    return {"message": "Project not found", "id": id}




# Comprar proyecto
def buy_project(project_id: int):
    projects = load_projects()
    player = load_player()

    # Buscar el proyecto por ID
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        return JSONResponse(
            {"message": "Project not found", "id": project_id},
            status_code=404
        )

    # Verificar si el proyecto ya está adquirido
    if project["acquired"]:
        return JSONResponse(
            {"message": "Project already acquired", "project": project},
            status_code=400
        )

    # Verificar si el jugador tiene suficiente dinero
    if player["money"] < project["price"]:
        return JSONResponse(
            {"message": "No tienes dinero suficiente. 📉", "player_money": player["money"]},
            status_code=422
        )

    # Restar el precio del proyecto al dinero del jugador y actualizar el proyecto
    player["money"] -= project["price"]
    project["acquired"] = True

   # Cargar las eficiencias y actualizar los puntos correspondientes
    efficiencies = load_efficiencies()

    # Verificar si la eficiencia asociada existe
    efficiency_index = project_id - 1  # Ajuste para indexado basado en ID del proyecto
    if 0 <= efficiency_index < len(efficiencies):
        efficiencies[efficiency_index]["points"] += project["efficiency_points"]
        
        # Guardar los cambios en el archivo de eficiencias
        with open(efficiencies_file_path, 'w', encoding='utf-8') as f:
            json.dump(efficiencies, f, indent=4, ensure_ascii=False)
    else:
        return JSONResponse(
            {"message": "Eficiencia asociada no encontrada", "project_id": project_id},
            status_code=404
        )

    # Guardar los cambios en el archivo de proyectos
    with open(projects_file_path, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=4, ensure_ascii=False)

    # Guardar los cambios del jugador
    save_player(player)

    return {
        "message": f"Project {project_id} acquired successfully",
        "player": player,
        "project": project,
    }