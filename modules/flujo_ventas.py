import json
import os

# Ruta del flujo de ventas
FLUJO_VENTAS_PATH = os.path.join(os.getcwd(), "flujo_ventas.json")

def cargar_flujo_ventas():
    """Carga el flujo de ventas desde un archivo JSON."""
    try:
        with open(FLUJO_VENTAS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "⚠️ No se encontró el archivo de flujo de ventas."}
    except json.JSONDecodeError:
        return {"error": "⚠️ Error en el formato del flujo de ventas."}

def obtener_paso_flujo(estado):
    """Obtiene la respuesta correspondiente al estado actual del usuario."""
    flujo = cargar_flujo_ventas()
    
    if "error" in flujo:
        return flujo["error"]
    
    return flujo.get(estado, "🤖 No tengo una respuesta para este paso. ¿Podrías darme más detalles?")
