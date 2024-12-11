from app.models import Player
import json
import os

# Ruta del archivo JSON
data_folder = os.path.join(os.path.dirname(__file__), "../data")
player_file_path = os.path.join(data_folder, "player.json")

# Cargar los datos del jugador
def load_player():
    with open(player_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Guardar los datos del jugador
def save_player(player_data):
    with open(player_file_path, 'w', encoding='utf-8') as f:
        json.dump(player_data, f, indent=4, ensure_ascii=False)

# Obtener los datos del jugador
def get_player():
    return load_player()

def set_player_data(player: Player):  # Aceptamos el objeto 'player' completo
    player_data = load_player()
    player_data["name"] = player.name
    player_data["money"] = player.money
    player_data["score"] = player.score
    save_player(player_data)  # Guardamos los cambios
    return {"message": "Player data updated", "player": player_data}


#FUNCIONES PUT

# Actualizar solo el nombre del jugador
def set_player_name(name: str):
    player_data = load_player()
    player_data["name"] = name
    save_player(player_data)
    return {"message": "Player name updated", "player": player_data}

# Actualizar solo el dinero del jugador
def set_player_money(money: int):
    player_data = load_player()
    player_data["money"] = money
    save_player(player_data)
    return {"message": "Player money updated", "player": player_data}

# Actualizar solo el puntaje del jugador
def set_player_score(score: int):
    player_data = load_player()
    player_data["score"] = score
    save_player(player_data)
    return {"message": "Player score updated", "player": player_data}

#FUNCIONS PUT

# Actualizar solo el nombre del jugador (PUT)
def update_player_name(name: str):
    player_data = load_player()
    player_data["name"] = name
    save_player(player_data)
    return {"message": "Player name updated via PUT", "player": player_data}

# Actualizar solo el dinero del jugador (PUT)
def update_player_money(money: int):
    player_data = load_player()
    player_data["money"] = money
    save_player(player_data)
    return {"message": "Player money updated via PUT", "player": player_data}

# Actualizar solo el puntaje del jugador (PUT)
def update_player_score(score: int):
    player_data = load_player()
    player_data["score"] = score
    save_player(player_data)
    return {"message": "Player score updated via PUT", "player": player_data}


# Establecer o actualizar los datos del jugador
def update_player_data(player: Player):
    # Actualizar todos los campos de los datos del jugador
    player_data = load_player()
    player_data["name"] = player.name
    player_data["money"] = player.money
    player_data["score"] = player.score
    save_player(player_data)  # Guardar los cambios
    return {"message": "Player data updated", "player": player_data}