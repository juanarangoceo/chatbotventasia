import openai
import os
from dotenv import load_dotenv
from modules.config_loader import cargar_prompt

# Cargar variables de entorno
load_dotenv()

# Configurar API Key de OpenAI
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: No se encontró la API Key en el archivo .env")

# Instanciar cliente OpenAI con la nueva API
client = openai.OpenAI(api_key=api_key)

# Cargar configuración desde prompt.json
config = cargar_prompt()

def construir_prompt():
    """Genera el prompt uniendo las secciones de prompt.json."""
    return f"""
    Nombre del Chatbot: {config.get('chatbot_name', 'Juan')}
    Rol: {config.get('role', 'Asistente Virtual de Ventas')}
    Estrategia de Ventas: {config.get('sales_strategy', 'Guiar al cliente a la compra con preguntas estratégicas')}
    Directrices de Respuesta: {config.get('response_guidelines', 'Respuestas claras y directas')}
    Manejo de Objeciones: {config.get('objections_handling', 'Resolver dudas sobre precio y funcionalidad del producto')}
    Método de Pago: {config.get('payment_method', 'Pago contra entrega en toda Colombia')}
    Política de Envíos: {config.get('shipping_policy', 'Envío gratuito con pago contra entrega en ciertas ciudades')}
    
    📌 Producto en Venta: {config.get('product_specs', {}).get('name', 'Máquina para Café Automática')}
    🔹 Potencia: {config.get('product_specs', {}).get('power', '850W')}
    🔹 Presión: {config.get('product_specs', {}).get('pressure', '15 bar')}
    🔹 Funciones: {', '.join(config.get('product_specs', {}).get('functions', []))}
    """

def generar_respuesta_ia(mensaje):
    """Genera una respuesta con OpenAI basada en el prompt estructurado."""
    try:
        response = client.chat.completions.create(
            model=config.get("modelo", "gpt-4"),
            messages=[
                {"role": "system", "content": construir_prompt()},
                {"role": "user", "content": mensaje}
            ],
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 300)
        )
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        return f"⚠️ Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde. Detalle: {str(e)}"
