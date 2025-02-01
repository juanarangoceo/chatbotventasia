import json
import os

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

def cargar_especificaciones_producto():
    """Carga la información del producto en cada consulta."""
    try:
        with open(PRODUCTO_JSON_PATH, "r", encoding="utf-8") as archivo:
            return json.load(archivo)  # Se carga directamente sin almacenar en caché
    except FileNotFoundError:
        return {"error": "⚠️ No se encontró la información del producto en 'producto.json'."}
    except json.JSONDecodeError:
        return {"error": "⚠️ Error: 'producto.json' tiene un formato inválido."}
