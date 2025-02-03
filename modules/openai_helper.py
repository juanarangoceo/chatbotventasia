import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_prompt
from modules.producto_helper import cargar_especificaciones_producto

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

client = openai.OpenAI(api_key=api_key)
config = cargar_prompt()
producto = cargar_especificaciones_producto()

def generar_respuesta_ia(mensaje, historial):
    """Genera una respuesta utilizando OpenAI con el contexto del producto y el historial de la conversación."""
    try:
        if not config:
            return "⚠️ Error: No se pudo cargar la configuración del chatbot."

        if "nombre" not in producto:
            return "⚠️ Error: No se pudo cargar la información del producto."

        print(f"📡 Enviando mensaje a OpenAI: {mensaje}")  # DEBUG

        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {"role": "system", "content": f"Actúa como Juan, un asesor experto en café y ventas de cafeteras."},
                {"role": "user", "content": mensaje}
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=100  # Reducido para respuestas más concisas
        )
        
        respuesta = response.choices[0].message.content.strip()
        print(f"✅ Respuesta de OpenAI: {respuesta}")  # DEBUG
        return respuesta

    except openai.OpenAIError as e:
        print(f"❌ ERROR en OpenAI: {str(e)}")
        return "⚠️ Lo siento, hay un problema con el sistema. ¿Cómo puedo ayudarte con la cafetera?"

    except Exception as e:
        print(f"❌ ERROR inesperado en OpenAI: {str(e)}")
        return "⚠️ Lo siento, hubo un problema técnico. ¿Te gustaría saber más sobre la cafetera? ☕"
