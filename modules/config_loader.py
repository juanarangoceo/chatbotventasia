import json
import os

CONFIG_JSON_PATH = os.path.join(os.getcwd(), "config.json")

def cargar_config():
    """Carga siempre la configuración más reciente desde config.json."""
    try:
        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)  # Se carga directamente, sin caché
    except FileNotFoundError:
        print("⚠️ Error: No se encontró 'config.json'.")
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error: El archivo 'config.json' tiene un formato inválido.")
        return {}

# Función opcional para forzar recarga si es necesario en otro módulo
def recargar_config():
    """Función auxiliar para forzar la recarga de la configuración en tiempo real."""
    return cargar_config()
