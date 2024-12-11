import json
import os

# Ruta del archivo JSON de eficiencias
data_folder = os.path.join(os.path.dirname(__file__), "../data")
efficiencies_file_path = os.path.join(data_folder, "eficiencias.json")

# Cargar las eficiencias desde el archivo JSON
def load_efficiencies():
    with open(efficiencies_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Obtener las eficiencias
def get_efficiencies():
    efficiencies = load_efficiencies()
    return {"efficiencies": efficiencies}

# Agregar una nueva eficiencia
def add_efficiency(efficiency: dict):
    efficiencies = load_efficiencies()
    new_id = max([e["id"] for e in efficiencies]) + 1 if efficiencies else 1
    efficiency["id"] = new_id
    efficiency["points"] = efficiency.get("points", 0)  # Asigna 0 si no está presente
    efficiencies.append(efficiency)
    
    # Guardar la nueva eficiencia en el archivo JSON
    with open(efficiencies_file_path, 'w', encoding='utf-8') as f:
        json.dump(efficiencies, f, indent=4, ensure_ascii=False)
    
    return {"message": "Efficiency added successfully", "efficiency": efficiency}


# Actualizar el campo 'points' de una eficiencia
def update_efficiency_points(id: int, points: int):
    if points > 36:
        return {"message": "Points cannot exceed the maximum limit of 36", "id": id, "points": points}
    
    efficiencies = load_efficiencies()
    
    # Buscar la eficiencia por 'id'
    for efficiency in efficiencies:
        if efficiency["id"] == id:
            efficiency["points"] = points
            # Guardar las eficiencias actualizadas en el archivo JSON
            with open(efficiencies_file_path, 'w', encoding='utf-8') as f:
                json.dump(efficiencies, f, indent=4, ensure_ascii=False)
            return {"message": f"Efficiency points updated for id {id}", "efficiency": efficiency}
    
    return {"message": "Efficiency not found", "id": id}