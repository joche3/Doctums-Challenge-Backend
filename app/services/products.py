import json
import os
from app.services.player import load_player, save_player
from fastapi.responses import JSONResponse
from app.services.efficiencies import load_efficiencies, efficiencies_file_path

# Ruta del archivo JSON
data_folder = os.path.join(os.path.dirname(__file__), "../data")
productos_file_path = os.path.join(data_folder, "productos.json")

# Cargar los productos desde el archivo JSON
def load_products():
    with open(productos_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Obtener los productos
def get_products():
    productos = load_products()
    return {"products": productos}

# Agregar un nuevo producto
def add_product(product: dict):
    productos = load_products()
    new_id = max([p["id"] for p in productos]) + 1 if productos else 1
    product["id"] = new_id
    product["acquired"] = product.get("acquired", False)  # Asigna False si no está presente
    product["efficiency_points"] = product.get("efficiency_points", 0)  # Asigna 0 si no está presente
    productos.append(product)
    
    # Guardar el nuevo producto en el archivo JSON
    with open(productos_file_path, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)
    
    return {"message": "Producto agregado con éxito", "product": product}

# Actualizar el campo 'acquired' de un producto
def update_product_acquired(id: int, acquired: bool):
    productos = load_products()

    # Buscar el producto por 'id'
    for product in productos:
        if product["id"] == id:
            product["acquired"] = acquired
            # Guardar los productos actualizados en el archivo JSON
            with open(productos_file_path, 'w', encoding='utf-8') as f:
                json.dump(productos, f, indent=4, ensure_ascii=False)
            return {"message": f"Product 'acquired' field updated for id {id}", "product": product}

    return {"message": "Product not found", "id": id}

# Comprar producto
def buy_product(product_id: int):
    productos = load_products()
    player = load_player()  # Suponiendo que tienes una función load_player para obtener los datos del jugador

    # Buscar el producto por ID
    product = next((p for p in productos if p["id"] == product_id), None)
    if not product:
        return JSONResponse(
            {"message": "Product not found", "id": product_id},
            status_code=404
        )

    # Verificar si el producto ya está adquirido
    if product["acquired"]:
        return JSONResponse(
            {"message": "Product already acquired", "product": product},
            status_code=400
        )

    # Verificar si el jugador tiene suficiente dinero
    if player["money"] < product["price"]:
        return JSONResponse(
            {"message": "No tienes dinero suficiente. 📉", "player_money": player["money"]},
            status_code=422
        )

    # Restar el precio del producto al dinero del jugador y actualizar el producto
    player["money"] -= product["price"]
    product["acquired"] = True

  # Cargar las eficiencias y actualizar los puntos correspondientes
    efficiencies = load_efficiencies()

    # Implementar la lógica cíclica para asignar puntos a las eficiencias
    num_efficiencies = len(efficiencies)  # Cantidad total de eficiencias
    efficiency_index = (product_id - 1) % num_efficiencies  # Índice cíclico basado en ID del producto

    # Actualizar los puntos de la eficiencia correspondiente
    efficiencies[efficiency_index]["points"] += product["efficiency_points"]

    # Guardar los cambios en el archivo de eficiencias
    with open(efficiencies_file_path, 'w', encoding='utf-8') as f:
        json.dump(efficiencies, f, indent=4, ensure_ascii=False)

    # Guardar los cambios del jugador
    save_player(player)
    
    # Guardar los cambios en el archivo de productos
    with open(productos_file_path, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

    return JSONResponse(
        {
            "message": f"Product {product_id} acquired successfully",
            "player": player,
            "product": product,
        },
        status_code=200
    )