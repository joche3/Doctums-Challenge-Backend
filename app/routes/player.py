from fastapi import APIRouter, Body
from app.services.player import get_player, set_player_data, update_player_data, set_player_name, set_player_money, set_player_score
from app.models import Player  # Importar el modelo Player

router = APIRouter()

# Ruta para obtener los datos del jugador
@router.get("/player")
def get_player_route():
    return get_player()

@router.post("/player")
def set_player_data_route(player: Player):  # Aceptamos el objeto 'Player' completo
    return set_player_data(player)


# Nuevas rutas POST para actualizar campos individuales
@router.post("/playerName")
def set_player_name_route(name: str = Body(...)):  # Aceptamos solo 'name'
    return set_player_name(name)

@router.post("/playerMoney")
def set_player_money_route(money: int = Body(...)):  # Aceptamos solo 'money'
    return set_player_money(money)

@router.post("/playerScore")
def set_player_score_route(score: int = Body(...)):  # Aceptamos solo 'score'
    return set_player_score(score)



# Función PUT para actualizar todos los datos del jugador
@router.put("/player")
def update_player_route(player: Player):  # Usamos Player para recibir todos los datos
    return update_player_data(player)  # Actualizamos todos los datos del jugador