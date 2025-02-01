import json
import os
import time  
from modules.producto_helper import cargar_especificaciones_producto  

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

# Diccionario para manejar las sesiones activas de clientes
sesiones = {}

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes. ¿En qué podemos ayudarte hoy?",
    "ubicacion": "📍 Estamos ubicados en Bogotá, Colombia. ¿Te gustaría saber si hacemos envíos a tu ciudad?",
    "precio": "💰 Nuestros precios varían según el producto. ¿Te gustaría conocer más detalles sobre el producto?",
}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Maneja la conversación del chatbot de forma natural, asegurando una experiencia fluida para el cliente."""
    time.sleep(3)  # ⏳ Simula un tiempo de respuesta natural
    mensaje = mensaje.lower().strip()
    
    # Manejo de sesión del cliente
    if cliente_id not in sesiones:
        sesiones[cliente_id] = {"paso": 0, "datos": {}}

    paso = sesiones[cliente_id]["paso"]
    datos = sesiones[cliente_id]["datos"]

    # 📌 Responder preguntas sobre el producto en cualquier momento
    if "especificaciones" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = f"☕ *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "¿Te gustaría adquirirlo? 😊"

        return respuesta

    # 📌 Verificar si el cliente está en medio de la compra y responder preguntas sin perder el flujo
    if paso > 0 and any(palabra in mensaje for palabra in RESPUESTAS_PREDEFINIDAS.keys()):
        return RESPUESTAS_PREDEFINIDAS.get(mensaje, "¿Cómo más puedo ayudarte? 😊")

    # 📌 Flujo de venta natural, permitiendo preguntas en cualquier momento
    if "quiero comprar" in mensaje or "cómo lo adquiero" in mensaje:
        sesiones[cliente_id]["paso"] = 1
        return "¡Genial! Para proceder con la compra, ¿cuál es tu nombre? 😊"

    if paso == 1:
        datos["nombre"] = mensaje
        sesiones[cliente_id]["paso"] = 2
        return f"¡Gracias {datos['nombre']}! Ahora dime tu número de teléfono 📞."

    if paso == 2:
        if not mensaje.isdigit():
            return "📞 El número de teléfono debe contener solo dígitos. ¿Podrías ingresarlo nuevamente?"
        datos["telefono"] = mensaje
        sesiones[cliente_id]["paso"] = 3
        return "¿En qué ciudad te encuentras? 🏙️"

    if paso == 3:
        datos["ciudad"] = mensaje
        sesiones[cliente_id]["paso"] = 4
        return "¡Casi terminamos! Ahora, necesito la dirección exacta para el envío. 📦"

    if paso == 4:
        datos["direccion"] = mensaje
        sesiones[cliente_id]["paso"] = 5
        return f"✅ ¡Gracias {datos['nombre']}! Tu pedido será enviado a {datos['direccion']}. Te contactaremos al {datos['telefono']}."

    # 📌 Si el mensaje no se reconoce, sugerir opciones sin interrumpir la venta
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta? También puedo ayudarte con información sobre el producto o el proceso de compra."
