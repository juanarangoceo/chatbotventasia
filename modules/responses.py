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
    "leche": "Sí, la *Cafetera Espresso Pro* tiene un espumador de leche 🥛 para texturas perfectas. ¿Quieres que te ayude con tu pedido? 📦",
    "precio": "La *Cafetera Espresso Pro* cuesta *399,900 COP* 💰 con *envío gratis* 🚚. ¿Deseas que la enviemos a tu domicilio? 🏡",
    "garantía": "Tiene *6 meses de garantía* 🔧 por defectos de fábrica. Es un equipo duradero y confiable. ¿Te gustaría ordenar la tuya hoy? ☕",
}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la conversación asegurando que el chatbot siga vendiendo siempre."""

    time.sleep(2)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🔹 Si el usuario es nuevo, iniciar con saludo y pregunta de ciudad
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy Juan, experto en café. Te ayudaré con la *Cafetera Espresso Pro*. 🙌\n\n"
            "✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
        )

    # 🔹 Guardar ciudad y avanzar en el flujo
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.title()
        usuarios[cliente_id]["estado"] = "confirmar_interes"
        return (
            f"¡Genial! Enviamos a {mensaje.title()} con *pago contra entrega* 🚛.\n\n"
            "👉 *¿Te gustaría conocer más sobre la Cafetera Espresso Pro?*"
        )

    # 🔹 Si el usuario confirma interés, explicar beneficios en una respuesta corta
    if usuarios[cliente_id]["estado"] == "confirmar_interes" and mensaje in ["sí", "si", "claro", "me gustaría saber más"]:
        usuarios[cliente_id]["estado"] = "explicar_beneficios"
        return (
            "🔹 La *Cafetera Espresso Pro* tiene:\n"
            "- *15 bares de presión* para espressos perfectos ☕\n"
            "- *Espumador de leche* 🥛 para capuchinos cremosos\n"
            "- *Fácil de usar* con pantalla táctil\n\n"
            "✅ *¿Te gustaría recibirla con pago contra entrega?*"
        )

    # 🔹 Si el usuario pregunta por características del producto
    if any(palabra in mensaje for palabra in ["características", "detalles", "qué incluye"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return "⚠️ Lo siento, hubo un error al cargar la información del producto."

        respuesta = (
            f"📦 *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
            "📌 *Características principales:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]])
            + f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
            "📦 *¿Quieres que la enviemos hoy mismo?* 🚛"
        )

        return respuesta

    # 🔹 Si la pregunta coincide con una de las preguntas clave, responder con información relevante y reforzar la venta
    for clave, respuesta in PREGUNTAS_CLAVE.items():
        if clave in mensaje:
            return respuesta

    # 🔹 Si el mensaje no encaja con ninguna respuesta, usar OpenAI con un prompt más controlado
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Eres Juan, un asesor de ventas especializado en la *Cafetera Espresso Pro*. "
                    "Tu único objetivo es vender este producto. Responde siempre con respuestas cortas, "
                    "claras y enfocadas en cerrar la venta. No menciones otros productos. "
                    "Si te hacen una pregunta, respóndela y luego lleva la conversación de vuelta a la compra."
                )},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.3,  # Reducir creatividad para respuestas más predecibles
            max_tokens=150
        )
        return response.choices[0].message.content.strip() + "\n\n📦 *¿Quieres que te ayude a realizar tu pedido?* 🚛"

    except openai.APIError:
        return "⚠️ Lo siento, hubo un problema con el servicio de OpenAI. Inténtalo más tarde."

