import json

def cargar_config():
    """Carga la configuración desde config.json."""
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)
