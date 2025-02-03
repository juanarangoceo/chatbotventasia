import json
import os

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

def cargar_especificaciones_producto():
    """Carga los datos del producto desde producto.json"""
    try:
        with open(PRODUCTO_JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "⚠️ No se encontró el archivo de especificaciones del producto."}
    except json.JSONDecodeError:
        return {"error": "⚠️ El archivo de producto tiene un formato incorrecto."}
