import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_prompt  # Ahora importamos cargar_prompt

# Cargar variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

# Cargar el prompt desde prompt.json
prompt_config = cargar_prompt()

def construir_prompt():
    """Genera el prompt uniendo las secciones de prompt.json."""
    return f"""
    Nombre del Chatbot: {prompt_config.get('Nombre del Chatbot', 'Asistente Virtual')}
    Rol: {prompt_config.get('Rol del Chatbot', 'Asesor de Ventas de Café')}
    Estrategia de Ventas: {prompt_config.get('Manejo de Conexiones de Ventas', '')}
    Formulación de Respuestas: {prompt_config.get('Formulación de Respuestas', '')}
    Manejo de Objeciones: {prompt_config.get('Manejo de Objeciones', '')}
    Información Técnica: {prompt_config.get('Ficha Técnica', '')}
    """

def generar_respuesta_ia(mensaje):
    """Genera una respuesta con OpenAI basada en el prompt estructurado."""
    try:
        response = openai.ChatCompletion.create(
            model=prompt_config.get("modelo", "gpt-4"),  # Usa el modelo definido en el prompt.json
            messages=[
                {"role": "system", "content": construir_prompt()},
                {"role": "user", "content": mensaje}
            ],
            temperature=prompt_config.get("temperature", 0.7),
            max_tokens=prompt_config.get("max_tokens", 300)
        )

        return response['choices'][0]['message']['content'].strip()

    except openai.error.OpenAIError as e:
        return "⚠️ Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde."

