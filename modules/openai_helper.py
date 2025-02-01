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

def generar_respuesta_ia(mensaje):
    """Genera una respuesta con OpenAI basada en el prompt estructurado."""
    try:
        client = openai.OpenAI()  # Inicializar el cliente OpenAI

        response = client.chat.completions.create(
            model=config["modelo"],
            messages=[
                {"role": "system", "content": config["prompt"]},
                {"role": "user", "content": mensaje}
            ],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        )

        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        print(f"❌ Error en OpenAI: {e}")
        return "Lo siento, hubo un problema con OpenAI. Inténtalo más tarde."
