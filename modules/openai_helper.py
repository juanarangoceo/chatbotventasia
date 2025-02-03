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
        # Verificar si la configuración se cargó correctamente
        if not config:
            return "⚠️ Error: No se pudo cargar la configuración del chatbot."

        if "nombre" not in producto:
            return "⚠️ Error: No se pudo cargar la información del producto."

        # Construcción del prompt para OpenAI
        prompt_base = f"""
        Actúa como *Juan*, un asesor experto en café y ventas de cafeteras. 
        Tu objetivo es guiar al cliente en la compra de la *{producto['nombre']}*.
        
        📌 **Características del producto:**
        - {producto['descripcion']}
        - Características: {", ".join(producto['caracteristicas'])}
        - 💰 *Precio:* {producto['precio']}
        - 🚛 *Envío:* {producto['envio']}
        
        📈 **Estrategia de ventas:**
        - Responde de manera *breve* (máximo 25 palabras).
        - Resalta palabras clave con *negritas*.
        - Siempre incluye una pregunta al final para avanzar la venta.
        - Si el cliente tiene dudas, refuerza los beneficios del producto.
        
        🔥 **Historial de la conversación:**
        {historial}
        """

        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {"role": "system", "content": prompt_base},
                {"role": "user", "content": mensaje}
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 250)
        )
        
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        return f"⚠️ Error en OpenAI: {str(e)}"
    except Exception as e:
        return f"⚠️ Error inesperado: {str(e)}"
