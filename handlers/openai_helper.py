import openai
import os
import json
from dotenv import load_dotenv
from handlers.producto_helper import cargar_especificaciones_producto

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

client = openai.OpenAI(api_key=api_key)

# Cargar prompt.json directamente
with open("prompt.json", "r", encoding="utf-8") as file:
    config = json.load(file)

producto = cargar_especificaciones_producto()

def generar_respuesta_ia(mensaje):
    """Genera una respuesta usando OpenAI, manteniendo el tono y propósito del chatbot."""
    try:
        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[{"role": "system", "content": "Eres Juan, asesor de café experto."}, {"role": "user", "content": mensaje}],
            temperature=config.get("temperature", 0.5),
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ ERROR en OpenAI: {str(e)}")
        return "⚠️ Lo siento, hubo un error. ¿Cómo puedo ayudarte?"
