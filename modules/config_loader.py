import json
import os

CONFIG_JSON_PATH = os.path.join(os.getcwd(), "config.json")

def cargar_config():
    """Carga la configuración desde config.json y maneja errores."""
    try:
        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("⚠️ Error: No se encontró 'config.json'.")
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error: El archivo 'config.json' tiene un formato inválido.")
        return {}
