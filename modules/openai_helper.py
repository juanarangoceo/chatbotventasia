import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_prompt

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

client = openai.OpenAI(api_key=api_key)
config = cargar_prompt()

def generar_respuesta_ia(mensaje):
    """Usa OpenAI para responder preguntas generales manteniendo el foco en la venta"""
    try:
        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {"role": "system", "content": "Responde de forma concisa y siempre guiando la conversación a vender la Cafetera Espresso Pro."},
                {"role": "user", "content": mensaje}
            ],
            temperature=config.get("temperature", 0.5),
            max_tokens=config.get("max_tokens", 200)
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        return f"⚠️ Lo siento, hubo un problema con OpenAI. Detalle: {str(e)}"
