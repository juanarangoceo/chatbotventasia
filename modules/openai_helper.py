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
    """Usa OpenAI para responder cualquier pregunta manteniendo el foco en la venta."""
    try:
        prompt = (
            f"{config.get('prompt')}\n\n"
            "Tu tarea es responder de manera fluida y natural a cualquier pregunta del cliente, "
            "pero siempre redirigiendo la conversación hacia la venta de la *Cafetera Espresso Pro*. "
            "Nunca hables de otros productos. Responde con mensajes cortos y persuasivos. "
            "El cliente escribió: " + mensaje
        )

        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[{"role": "system", "content": prompt}],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 250)
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        return f"⚠️ Lo siento, hubo un problema con OpenAI. Detalle: {str(e)}"
