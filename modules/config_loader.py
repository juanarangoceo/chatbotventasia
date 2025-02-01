import json
import os

PROMPT_JSON_PATH = os.path.join(os.getcwd(), "prompt.json")
prompt_cache = None  # Caché para evitar recargas innecesarias

def cargar_prompt():
    """Carga el prompt desde prompt.json y lo almacena en caché."""
    global prompt_cache
    if prompt_cache:
        return prompt_cache
    
    try:
        with open(PROMPT_JSON_PATH, "r", encoding="utf-8") as file:
            prompt_cache = json.load(file)
            return prompt_cache
    except FileNotFoundError:
        print("⚠️ Error: No se encontró 'prompt.json'.")
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error: El archivo 'prompt.json' tiene un formato inválido.")
        return {}
