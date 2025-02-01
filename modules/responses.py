import json
import os
import time
from modules.producto_helper import cargar_especificaciones_producto

# Almacena los clientes para controlar la primera interacción
usuarios = {}

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes. ¿En qué podemos ayudarte hoy?",
    "ubicacion": "📍 Estamos ubicados en Bogotá, Colombia. ¿Desde qué ciudad nos escribes?",
}

DATOS_CLIENTE = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona la respuesta y el flujo de ventas de manera estructurada."""
    
    time.sleep(3)  # ⏳ Simula un tiempo de respuesta
    
    mensaje = mensaje.lower().strip()

    # 🔹 Saludo y pregunta inicial si es un nuevo usuario
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte a disfrutar un café de calidad en casa. 🙌\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
    
    # 🔹 Si el usuario ya respondió con una ciudad, activar el flujo de ventas
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["estado"] = "flujo_ventas"
        return "¡Gracias! Enviamos a tu ciudad con *pago contra entrega* 🚛.\n¿Te gustaría conocer más sobre nuestra *Máquina para Café Automática*?"

    # 🔹 Detectar intención de conocer especificaciones del producto
    if "especificaciones" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = f"☕ *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "¿Te gustaría que te ayudemos a realizar tu compra? 😊"

        return respuesta

    # 🔹 Respuesta por defecto para mantener la conversación activa
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
