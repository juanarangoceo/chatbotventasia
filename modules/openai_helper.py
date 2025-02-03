import openai
import os
import json
from dotenv import load_dotenv
from modules.producto_helper import cargar_especificaciones_producto

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

def generar_respuesta_ia(mensaje, historial):
    """Genera una respuesta utilizando OpenAI con el contexto del producto."""
    try:
        print(f"📡 Enviando mensaje a OpenAI: {mensaje}")  # DEBUG

        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[{"role": "system", "content": "Asesor experto en café."}, {"role": "user", "content": mensaje}],
            temperature=config.get("temperature", 0.7),
            max_tokens=100
        )
        
        respuesta = response.choices[0].message.content.strip()
        print(f"✅ Respuesta de OpenAI: {respuesta}")  # DEBUG
        return respuesta

    except Exception as e:
        print(f"❌ ERROR en OpenAI: {str(e)}")
        return "⚠️ Parece que tenemos problemas técnicos. ¿Cómo puedo ayudarte con la cafetera?"
