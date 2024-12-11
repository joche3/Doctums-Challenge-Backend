import json
import os
from app.services.player import load_player, save_player
from fastapi.responses import JSONResponse
from app.services.efficiencies import load_efficiencies, efficiencies_file_path


# Ruta del archivo JSON de recursos
data_folder = os.path.join(os.path.dirname(__file__), "../data")
resources_file_path = os.path.join(data_folder, "recursos.json")

# Cargar los recursos desde el archivo JSON
def load_resources():
    with open(resources_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Obtener los recursos
def get_resources():
    resources = load_resources()
    return {"resources": resources}

# Agregar un nuevo recurso
def add_resource(resource: dict):
    resources = load_resources()
    new_id = max([r["id"] for r in resources]) + 1 if resources else 1
    resource["id"] = new_id
    resource["efficiency_points"] = resource.get("efficiency_points", 0)  # Inicializado en 0 si no está presente
    resource["acquired"] = resource.get("acquired", False)  # Inicializado en False si no está presente
    resources.append(resource)

    # Guardar el nuevo recurso en el archivo JSON
    with open(resources_file_path, 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=4, ensure_ascii=False)

    return {"message": "Resource added successfully", "resource": resource}

# Actualizar el campo 'acquired' de un recurso
def update_resource_acquired(id: int, acquired: bool):
    resources = load_resources()

    # Buscar el recurso por 'id'
    for resource in resources:
        if resource["id"] == id:
            resource["acquired"] = acquired
            # Guardar los recursos actualizados en el archivo JSON
            with open(resources_file_path, 'w', encoding='utf-8') as f:
                json.dump(resources, f, indent=4, ensure_ascii=False)
            return {"message": f"Resource 'acquired' field updated for id {id}", "resource": resource}

    return {"message": "Resource not found", "id": id}

# Comprar recurso
def buy_resource(resource_id: int):
    resources = load_resources()
    player = load_player()

    # Buscar el recurso por ID
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if not resource:
        return JSONResponse(
            {"message": "Resource not found", "id": resource_id},
            status_code=404
        )

    # Verificar si el recurso ya está adquirido
    if resource["acquired"]:
        return JSONResponse(
            {"message": "Resource already acquired", "resource": resource},
            status_code=400
        )

    # Verificar si el jugador tiene suficiente dinero
    if player["money"] < resource["price"]:
        return JSONResponse(
            {"message": "No tienes dinero suficiente. 📉", "player_money": player["money"]},
            status_code=422
        )

    # Restar el precio del recurso al dinero del jugador y actualizar el recurso
    player["money"] -= resource["price"]
    resource["acquired"] = True


  # Cargar las eficiencias y actualizar los puntos correspondientes
    efficiencies = load_efficiencies()

    # Determinar la eficiencia asociada basada en la lógica de desplazamiento
    efficiency_index = resource_id + 6  # Ajustar el índice (recurso 1 -> eficiencia 6, recurso 2 -> eficiencia 7, etc.)
    if 0 <= efficiency_index - 1 < len(efficiencies):  # Verificar si el índice está dentro del rango
        efficiencies[efficiency_index - 1]["points"] += resource["efficiency_points"]

        # Guardar los cambios en el archivo de eficiencias
        with open(efficiencies_file_path, 'w', encoding='utf-8') as f:
            json.dump(efficiencies, f, indent=4, ensure_ascii=False)
    else:
        return JSONResponse(
            {"message": "Eficiencia asociada no encontrada", "resource_id": resource_id},
            status_code=404
        )

    # Guardar los cambios en el archivo de recursos
    with open(resources_file_path, 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=4, ensure_ascii=False)

    # Guardar los cambios del jugador
    save_player(player)

    return {
        "message": f"Resource {resource_id} acquired successfully",
        "player": player,
        "resource": resource,
    }
