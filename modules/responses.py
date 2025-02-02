import json
import os
import time
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

# Almacena los clientes y el estado de su conversación
usuarios = {}

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes. ¿En qué podemos ayudarte hoy?",
    "ubicacion": "📍 Estamos ubicados en Bogotá, Colombia. ¿Desde qué ciudad nos escribes?",
}

DATOS_CLIENTE = {}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la respuesta del chatbot con lógica estructurada para ventas."""
    
    time.sleep(3)  # ⏳ Simula un tiempo de respuesta para mayor realismo
    mensaje = mensaje.lower().strip()

    # 🔹 Primera interacción: Saludo exacto y pregunta de ciudad
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte a descubrir cómo puedes disfrutar en casa de un café digno de cafetería, con nuestra Máquina para Café Automática. 🙌\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
    
    # 🔹 Validar respuesta de ciudad y continuar con la venta
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["estado"] = "flujo_ventas"
        return "¡Gracias! Enviamos a tu ciudad con *pago contra entrega* 🚛. \n" \
               "¿Te gustaría conocer más sobre nuestra *Máquina para Café Automática* y cómo puede mejorar tu rutina diaria?"

    # 🔹 Intentar respuestas predefinidas antes de usar IA
    for palabra_clave, respuesta in RESPUESTAS_PREDEFINIDAS.items():
        if palabra_clave in mensaje:
            return respuesta

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

    # 🔹 Usar IA para continuar la conversación de manera natural
    return generar_respuesta_ia(mensaje)
