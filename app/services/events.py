import json
import os
from fastapi.responses import JSONResponse

# Ruta del archivo JSON de eventos
data_folder = os.path.join(os.path.dirname(__file__), "../data")
events_file_path = os.path.join(data_folder, "eventos.json")

# Cargar los eventos desde el archivo JSON
def load_events():
    with open(events_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Obtener todos los eventos
def get_events():
    events = load_events()
    return {"events": events}

# Agregar un nuevo evento
def add_event(event: dict):
    events = load_events()
    new_id = max([e["id"] for e in events]) + 1 if events else 1
    event["id"] = new_id
    events.append(event)

    # Guardar el nuevo evento en el archivo JSON
    with open(events_file_path, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

    return {"message": "Event added successfully", "event": event}

# Actualizar un evento existente
def update_event(id: int, updated_event: dict):
    events = load_events()

    # Buscar el evento por 'id'
    for event in events:
        if event["id"] == id:
            event.update(updated_event)
            # Guardar los eventos actualizados en el archivo JSON
            with open(events_file_path, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=4, ensure_ascii=False)
            return {"message": f"Event updated successfully for id {id}", "event": event}

    return {"message": "Event not found", "id": id}

# Eliminar un evento
def delete_event(id: int):
    events = load_events()

    # Filtrar el evento que se desea eliminar
    events = [event for event in events if event["id"] != id]

    # Guardar los eventos actualizados en el archivo JSON
    with open(events_file_path, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

    return {"message": f"Event with id {id} deleted successfully"}