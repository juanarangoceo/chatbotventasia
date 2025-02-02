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

# Preguntas clave para guiar la conversación
PREGUNTAS_CLAVE = {
    "leche": "Sí, la *Cafetera Espresso Pro* tiene un espumador de leche 🥛 para texturas perfectas. ¿Quieres que te ayude con tu pedido? 📦",
    "precio": "La *Cafetera Espresso Pro* cuesta *399,900 COP* 💰 con *envío gratis* 🚚. ¿Deseas que la enviemos a tu domicilio? 🏡",
    "garantía": "Tiene *6 meses de garantía* 🔧 por defectos de fábrica. Es un equipo duradero y confiable. ¿Te gustaría ordenar la tuya hoy? ☕",
}

# Datos que el chatbot debe recolectar para cerrar la venta
CAMPOS_DATOS = ["nombre", "teléfono", "ciudad", "dirección"]

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la conversación asegurando que el chatbot siga vendiendo siempre."""
    time.sleep(2)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🔹 Si el usuario es nuevo, iniciar con saludo y pregunta de ciudad
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad", "datos": {}}
        return (
            "¡Hola! ☕ Soy Juan, experto en café. Te ayudaré con la *Cafetera Espresso Pro*. 🙌\n\n"
            "✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
        )

    # 🔹 Guardar ciudad y avanzar en el flujo
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["datos"]["ciudad"] = mensaje.title()
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

    # 🔹 Si el cliente dice que quiere comprar, pedir datos en orden
    if "quiero comprar" in mensaje or "sí" in mensaje and usuarios[cliente_id]["estado"] in ["explicar_beneficios", "resolver_objeciones"]:
        usuarios[cliente_id]["estado"] = "solicitar_datos"
        usuarios[cliente_id]["datos_pendientes"] = CAMPOS_DATOS.copy()
        return "📋 Para procesar tu pedido, necesito algunos datos:\n\n" + pedir_siguiente_dato(cliente_id)

    # 🔹 Recolectar datos del cliente
    if usuarios[cliente_id]["estado"] == "solicitar_datos":
        campo_actual = usuarios[cliente_id]["datos_pendientes"].pop(0)
        usuarios[cliente_id]["datos"][campo_actual] = mensaje

        # Si faltan más datos, seguir pidiendo
        if usuarios[cliente_id]["datos_pendientes"]:
            return pedir_siguiente_dato(cliente_id)

        # Si ya se recolectaron todos los datos, confirmar la compra
        usuarios[cliente_id]["estado"] = "confirmar_datos"
        return confirmar_datos(cliente_id)

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

def pedir_siguiente_dato(cliente_id):
    """Solicita el siguiente dato necesario para procesar la compra."""
    campo = usuarios[cliente_id]["datos_pendientes"][0]
    preguntas = {
        "nombre": "😊 ¿Cuál es tu *nombre completo*?",
        "teléfono": "📞 ¿Cuál es tu *número de teléfono*?",
        "dirección": "🏡 ¿Cuál es la *dirección exacta* para la entrega?",
    }
    return preguntas.get(campo, "Por favor, proporciona el siguiente dato.")

def confirmar_datos(cliente_id):
    """Confirma los datos proporcionados por el cliente y cierra la venta."""
    datos = usuarios[cliente_id]["datos"]
    return (
        "✅ *Confirmemos tu pedido:* \n"
        f"👤 *Nombre:* {datos['nombre']}\n"
        f"📞 *Teléfono:* {datos['teléfono']}\n"
        f"🏙️ *Ciudad:* {datos['ciudad']}\n"
        f"🏡 *Dirección:* {datos['dirección']}\n\n"
        "📦 *Total a pagar:* 399,900 COP al recibir.\n\n"
        "¿Todo está correcto para finalizar tu compra? 🎉"
    )
