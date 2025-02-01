import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_config

# Cargar variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

# Instanciar cliente OpenAI con la nueva API
client = openai.OpenAI(api_key=api_key)

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
        response = client.chat.completions.create(
            model=config["modelo"],
            messages=[
                {"role": "system", "content": construir_prompt()},
                {"role": "user", "content": mensaje}
            ],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        return f"⚠️ Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde. Detalle: {str(e)}"
