import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_config
from openai import OpenAIError  # ✅ Importación correcta de OpenAIError

# Cargar variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

# Cargar configuración desde config.json
config = cargar_config()

def construir_prompt():
    """Genera el prompt uniendo las secciones de config.json para estructurar mejor la respuesta de OpenAI."""
    return f"""
    Nombre del Chatbot: {config.get('chatbot_name', 'Asistente de Ventas')}
    Rol: {config.get('role', 'Asistente Virtual de Ventas')}
    Objetivo: {config.get('objective', 'Ayudar a los clientes a elegir y comprar el producto')}
    Tono de conversación: {config.get('tone', 'Amigable, profesional y persuasivo')}
    Estrategia de Ventas: {config.get('sales_strategy', 'Guiar al cliente hacia la compra con un enfoque conversacional')}
    Directrices de Respuesta: {config.get('response_guidelines', 'Responder de manera clara y amigable, sin sonar robótico.')}
    """

def generar_respuesta_ia(mensaje):
    """Genera una respuesta con OpenAI basada en el prompt estructurado."""
    try:
        response = openai.ChatCompletion.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {"role": "system", "content": construir_prompt()},
                {"role": "user", "content": mensaje}
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 300)
        )

        return response['choices'][0]['message']['content'].strip()

    except OpenAIError as e:  # ✅ Captura correctamente errores de OpenAI
        print(f"❌ Error en OpenAI: {e}")  # Guarda el error en los logs de Render
        return "Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde."

