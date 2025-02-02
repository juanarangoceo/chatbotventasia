import time
from modules.flow_manager import actualizar_estado, obtener_estado, tiempo_desde_ultimo_mensaje
from modules.openai_helper import generar_respuesta_ia

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la conversación según el estado del cliente."""

    mensaje = mensaje.lower().strip()
    estado_actual = obtener_estado(cliente_id)

    # 🔹 Estado Inicial: Saludo y pregunta por la ciudad
    if estado_actual == "inicio":
        actualizar_estado(cliente_id, "preguntar_ciudad")
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte a descubrir cómo puedes disfrutar en casa de un café digno de cafetería, con nuestra *Cafetera Espresso Pro*.\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"

    # 🔹 Pregunta Ciudad: Responder con disponibilidad y avanzar al flujo de ventas
    if estado_actual == "preguntar_ciudad":
        actualizar_estado(cliente_id, "flujo_ventas")
        return f"¡Gracias! Enviamos a *{mensaje}* con *pago contra entrega* 🚛.\n¿Qué tipo de café disfrutas más en casa?"

    # 🔹 Flujo de ventas con OpenAI
    if estado_actual == "flujo_ventas":
        return generar_respuesta_ia(mensaje)

    # 🔹 Si el usuario no responde en 5 minutos, enviar recordatorio
    if tiempo_desde_ultimo_mensaje(cliente_id) > 300:
        return "¿Sigues ahí? ☕ ¿Te gustaría conocer más detalles sobre nuestra Cafetera Espresso Pro?"

    # 🔹 Respuesta por defecto
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles?"
