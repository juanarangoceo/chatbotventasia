import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_prompt

# Cargar variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

# Instanciar cliente OpenAI
client = openai.OpenAI(api_key=api_key)

# Cargar configuración desde prompt.json
config = cargar_prompt()

def construir_prompt():
    """Genera el prompt uniendo las secciones de prompt.json."""
    return f"""
    Nombre del Chatbot: {config.get('chatbot_name', 'Asistente')}
    Rol: {config.get('role', 'Asistente Virtual de Ventas')}
    Objetivo: {config.get('objective', 'Brindar información y cerrar ventas')}
    Tono de conversación: {config.get('tone', 'Amigable y profesional')}
    Estrategia de Ventas: {config.get('sales_strategy', 'Guiar al cliente a la compra con preguntas estratégicas')}
    Directrices de Respuesta: {config.get('response_guidelines', 'Respuestas claras y directas')}
    """

def generar_respuesta_ia(mensaje):
    """Genera una respuesta con OpenAI basada en el prompt estructurado."""
    try:
        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {"role": "system", "content": construir_prompt()},
                {"role": "user", "content": mensaje}
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 300)
        )
        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        return f"⚠️ Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde. Detalle: {str(e)}"
