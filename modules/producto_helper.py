import json
import os

# Definir la ruta correcta al archivo JSON en la raíz del proyecto
PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

def cargar_especificaciones_producto():
    """Carga la información del producto desde el archivo JSON en la raíz del proyecto."""
    try:
        with open(PRODUCTO_JSON_PATH, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"error": "No se encontró la información del producto en 'producto.json' en la raíz del proyecto."}
