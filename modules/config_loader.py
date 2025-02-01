import json
import os

CONFIG_JSON_PATH = os.path.join(os.getcwd(), "config.json")
config_cache = None  # Variable para almacenar la configuración en caché

def cargar_config():
    """Carga la configuración desde config.json y maneja errores."""
    global config_cache  # Usamos una variable global para almacenar la configuración

    # Si ya se cargó antes, devuelve la configuración desde la caché
    if config_cache:
        return config_cache

    try:
        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as file:
            config_cache = json.load(file)  # Guarda la configuración en caché
            return config_cache
    except FileNotFoundError:
        print("⚠️ Error: No se encontró 'config.json'.")
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error: El archivo 'config.json' tiene un formato inválido.")
        return {}

def recargar_config():
    """Fuerza la recarga de la configuración desde config.json."""
    global config_cache
    config_cache = None  # Borra la caché para que se vuelva a cargar
    return cargar_config()
