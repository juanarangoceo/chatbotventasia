import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_config

# Cargar variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

config = cargar_config()

def construir_prompt():
    """Genera el prompt uniendo las secciones de config.json."""
    return f"""
    Nombre del Chatbot: {config['chatbot_name']}
    Rol: {config['role']}
    Objetivo: {config['objective']}
    Tono de conversación: {config['tone']}
    Estrategia de Ventas: {config['sales_strategy']}
    Directrices de Respuesta: {config['response_guidelines']}
    """

def generar_respuesta_ia(mensaje):
    """Genera una respuesta con OpenAI basada en el prompt estructurado."""
    try:
        response = openai.ChatCompletion.create(
            model=config["modelo"],
            messages=[
                {"role": "system", "content": construir_prompt()},
                {"role": "user", "content": mensaje}
            ],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )

        return response['choices'][0]['message']['content'].strip()

    except openai.error.OpenAIError as e:
        return "Lo siento, hubo un problema con el servicio de OpenAI."
