import time
import threading
from modules.producto_helper import cargar_especificaciones_producto
from modules.config_loader import cargar_prompt

PROMPT = cargar_prompt()
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
    """Envía un mensaje si el cliente no responde en 5 minutos."""
    return "🤖 ¿Aún estás ahí? La *Máquina para Café Automática* está lista para enviarse. ¿Te gustaría concretar tu pedido ahora?"

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona la conversación utilizando prompt.json para guiar la venta."""
    time.sleep(3)
    mensaje = mensaje.lower().strip()

    if mensaje in ["hola", "buenas", "buen día", "buenas tardes", "buenas noches"]:
        return f"¡Hola! {PROMPT['guion_ventas']['interaccion_1']}"

    if "especificaciones" in mensaje or "detalles" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = f"☕ *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += f"{PROMPT['guion_ventas']['interaccion_2']}"

        iniciar_temporizador(cliente_id, enviar_mensaje_recordatorio)
        return respuesta

    for obj, resp in PROMPT["manejo_objeciones"].items():
        if obj in mensaje:
            return resp

    if "quiero comprar" in mensaje or "cómo lo adquiero" in mensaje:
        return PROMPT["guion_ventas"]["interaccion_3"]

    if cliente_id in DATOS_CLIENTE:
        datos_faltantes = ["nombre", "direccion", "telefono"]
        for key in datos_faltantes:
            if key not in DATOS_CLIENTE[cliente_id]:
                if key == "telefono" and not mensaje.isdigit():
                    return "📞 El número debe contener solo dígitos. ¿Podrías ingresarlo nuevamente?"

                DATOS_CLIENTE[cliente_id][key] = mensaje

                if all(d in DATOS_CLIENTE[cliente_id] for d in datos_faltantes):
                    pedido = DATOS_CLIENTE.pop(cliente_id)
                    return f"{PROMPT['mensaje_cierre']}"

                return PROMPT["guion_ventas"]["interaccion_4"]

    iniciar_temporizador(cliente_id, enviar_mensaje_recordatorio)
    return "🤖 No estoy seguro de haber entendido. ¿Te gustaría que te ayude con algo más?"
