import json
import os
import time
import threading
from modules.producto_helper import cargar_especificaciones_producto
from modules.config_loader import cargar_prompt

# Cargar el prompt desde el archivo JSON
PROMPT = cargar_prompt()

# Diccionario para almacenar datos del cliente
DATOS_CLIENTE = {}
TEMPORIZADORES = {}

def iniciar_temporizador(cliente_id, enviar_mensaje):
    """Inicia un temporizador de 5 minutos para enviar un recordatorio si el cliente no responde."""
    if cliente_id in TEMPORIZADORES:
        TEMPORIZADORES[cliente_id].cancel()

    timer = threading.Timer(300, enviar_mensaje, args=[cliente_id])
    TEMPORIZADORES[cliente_id] = timer
    timer.start()

def enviar_mensaje_recordatorio(cliente_id):
    """Envía un mensaje de seguimiento si el cliente no responde en 5 minutos."""
    return "🤖 ¿Aún estás ahí? La *Cafetera Espresso Pro* está lista para enviarse. ¿Te gustaría concretar tu pedido ahora?"

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona la conversación y evita repeticiones para concretar la venta."""
    time.sleep(3)  # ⏳ Retraso de 3 segundos antes de responder
    mensaje = mensaje.lower().strip()

    # Inicio de conversación con preguntas abiertas
    if mensaje in ["hola", "buenas", "buen día", "buenas tardes", "buenas noches"]:
        return "¡Hola! ¿Qué tipo de café prefieres: espresso, capuchino o americano? ☕"

    # Especificaciones del producto
    if "especificaciones" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = f"☕ *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "¿Te gustaría recibirla con *pago contra entrega*? 😊"

        iniciar_temporizador(cliente_id, enviar_mensaje_recordatorio)
        return respuesta

    # Manejo de objeciones
    objeciones = {
        "muy caro": "💰 Entiendo, pero esta cafetera tiene *calidad profesional* con *pantalla táctil y extracción de 20 Bar*. Además, el envío es gratis. ¿Te gustaría probarla?",
        "comparación": "🔍 A diferencia de otras, la *Cafetera Espresso Pro* tiene *pantalla táctil, tubo de vapor y sistema de extracción precisa*. ¿Quieres más detalles?",
        "quizás después": "😊 No hay problema. ¿Qué información te ayudaría a decidirte? Puedo responder cualquier duda."
    }
    for obj, resp in objeciones.items():
        if obj in mensaje:
            return resp

    # Proceso de venta: solicitar datos del cliente
    if "quiero comprar" in mensaje or "cómo lo adquiero" in mensaje:
        return solicitar_datos_venta(cliente_id)

    # Capturar información del cliente y validar datos
    if cliente_id in DATOS_CLIENTE:
        datos_faltantes = ["nombre", "direccion", "telefono", "unidades"]
        for key in datos_faltantes:
            if key not in DATOS_CLIENTE[cliente_id]:
                if key == "telefono" and not mensaje.isdigit():
                    return "📞 El número debe contener solo dígitos. ¿Podrías ingresarlo nuevamente?"

                DATOS_CLIENTE[cliente_id][key] = mensaje

                if all(d in DATOS_CLIENTE[cliente_id] for d in datos_faltantes):
                    pedido = DATOS_CLIENTE.pop(cliente_id)
                    return f"{PROMPT['mensaje_cierre']}"

                return solicitar_datos_venta(cliente_id)

    iniciar_temporizador(cliente_id, enviar_mensaje_recordatorio)
    return "🤖 No estoy seguro de haber entendido. ¿Te gustaría que te ayude con algo más?"
