import time
import json
import openai
from modules.producto_helper import cargar_especificaciones_producto
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Instanciar cliente OpenAI
client = openai.Client(api_key=api_key)

# Almacenar el estado de los clientes
usuarios = {}

# Respuestas predefinidas clave
PREGUNTAS_CLAVE = {
    "leche": "Sí, la *Cafetera Espresso Pro* tiene un tubo de vapor de acero inoxidable para crear espuma de leche perfecta. 🥛☕",
    "precio": "El precio de la *Cafetera Espresso Pro* es *399,900 COP* 💰 con *envío gratis a toda Colombia* 🚚.",
    "garantía": "La *Cafetera Espresso Pro* tiene garantía de *6 meses* por defectos de fábrica. 🔧📦",
}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la conversación y responde de forma inteligente."""

    time.sleep(2)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🔹 Si el usuario es nuevo, iniciar la conversación con el saludo correcto
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy Juan, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la *Cafetera Espresso Pro*. 🙌\n\n"
            "✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
        )

    # 🔹 Si está en la fase de preguntar la ciudad, guardar y avanzar
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.title()
        usuarios[cliente_id]["estado"] = "confirmar_interes"
        return (
            f"¡Gracias! Enviamos a {mensaje.title()} con *pago contra entrega* 🚛.\n\n"
            "¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*? ☕"
        )

    # 🔹 Si el usuario confirma interés, explicar beneficios
    if usuarios[cliente_id]["estado"] == "confirmar_interes" and mensaje in ["sí", "si", "claro", "me gustaría saber más"]:
        usuarios[cliente_id]["estado"] = "explicar_beneficios"
        return (
            "Nuestra *Cafetera Espresso Pro* ☕ tiene:\n"
            "- Presión de 15 bares para un espresso perfecto\n"
            "- Espumador de leche integrado 🥛\n"
            "- Preparación automática con un solo toque 🔘\n\n"
            "👉 *¿Prefieres café espresso o cappuccino?*"
        )

    # 🔹 Si el usuario pregunta por características del producto
    if any(palabra in mensaje for palabra in ["características", "detalles", "qué incluye"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return "⚠️ Lo siento, hubo un error al cargar la información del producto."

        respuesta = f"📦 *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "👉 *¿Quieres que te ayude a procesar tu pedido?* 📦"

        return respuesta

    # 🔹 Si la pregunta coincide con una de las preguntas clave, responder con información relevante
    for clave, respuesta in PREGUNTAS_CLAVE.items():
        if clave in mensaje:
            return respuesta

    # 🔹 Si el mensaje no encaja con ninguna respuesta, usar OpenAI para generar una respuesta natural
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Responde como un vendedor experto en cafeteras de forma clara y natural."},
                      {"role": "user", "content": mensaje}],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except openai.APIError:
        return "⚠️ Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde."

