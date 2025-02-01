import json
import os

CONFIG_JSON_PATH = os.path.join(os.getcwd(), "config.json")
PROMPT_JSON_PATH = os.path.join(os.getcwd(), "prompt.json")

def cargar_config():
    """Carga la configuración general desde config.json."""
    try:
        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def cargar_prompt():
    """Carga el prompt desde prompt.json."""
    try:
        with open(PROMPT_JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
