import json
import os

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