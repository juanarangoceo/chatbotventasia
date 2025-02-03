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
    """Genera respuestas concisas y persuasivas con OpenAI, siempre buscando vender la cafetera."""
    try:
        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Responde en un **tono conversacional corto y directo**. "
                        "Usa **negritas en palabras clave** como *precio*, *envío*, *beneficios* y *oferta*. "
                        "Siempre guía la conversación hacia la compra de la *Cafetera Espresso Pro*. "
                        "Ejemplo de respuesta: '**La Cafetera Espresso Pro** es ideal para hacer café de calidad en casa. "
                        "💰 **Precio:** 399,900 COP con 🚛 **envío gratis**. "
                        "¿Te gustaría aprovechar la oferta y recibirla en tu casa?'"
                    )
                },
                {"role": "user", "content": mensaje}
            ],
            temperature=0.4,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        return f"⚠️ Lo siento, hubo un problema con OpenAI. Detalle: {str(e)}"
