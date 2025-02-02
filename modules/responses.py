import time
from modules.flow_manager import actualizar_estado, obtener_estado

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes. ¿En qué podemos ayudarte hoy?",
    "ubicacion": "📍 Estamos en Bogotá, Colombia. ¿Desde qué ciudad nos escribes?",
}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la respuesta basada en el estado del usuario."""

    mensaje = mensaje.lower().strip()
    estado = obtener_estado(cliente_id)

    if estado == "inicio":
        actualizar_estado(cliente_id, "preguntar_ciudad")
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte con la Cafetera Espresso Pro. 🙌\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"

    if estado == "preguntar_ciudad":
        actualizar_estado(cliente_id, "flujo_ventas")
        return f"¡Gracias! Enviamos a {mensaje} con *pago contra entrega* 🚛.\n¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*?"

    if "cafetera" in mensaje:
        actualizar_estado(cliente_id, "flujo_ventas")
        return "La *Cafetera Espresso Pro* tiene 15 bares de presión y es ideal para preparar espresso y cappuccino. ☕\n¿Te gustaría recibirla con pago contra entrega? 😊"

    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
