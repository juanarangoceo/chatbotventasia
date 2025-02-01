import json
import os
import time
import threading  # Para manejar el temporizador
from modules.producto_helper import cargar_especificaciones_producto

# Definir la ruta correcta al archivo JSON en la raíz del proyecto
PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario es de 9 AM a 6 PM, lunes a viernes. ¿Quieres que gestionemos tu pedido hoy?",
    "ubicacion": "📍 Estamos en Bogotá y hacemos envíos a toda Colombia. ¿Te gustaría recibirlo en tu ciudad?",
    "precio": "💰 La *Cafetera Espresso Pro* cuesta $399,900 COP con envío gratis. ¿Quieres que la enviemos con pago contra entrega?",
}

DATOS_CLIENTE = {}
TEMPORIZADORES = {}

def iniciar_temporizador(cliente_id, enviar_mensaje):
    """Inicia un temporizador para enviar un mensaje si el cliente no responde en 5 minutos."""
    if cliente_id in TEMPORIZADORES:
        TEMPORIZADORES[cliente_id].cancel()

    timer = threading.Timer(300, enviar_mensaje, args=[cliente_id])  # 5 minutos (300 segundos)
    TEMPORIZADORES[cliente_id] = timer
    timer.start()

def enviar_mensaje_recordatorio(cliente_id):
    """Envía un mensaje de seguimiento si el cliente no responde en 5 minutos."""
    return f"🤖 ¡Aún estás ahí? La *Cafetera Espresso Pro* está lista para enviarse. ¿Te gustaría concretar tu pedido?"

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona la conversación guiada, manejo de objeciones y cierre de ventas."""
    time.sleep(3)  # ⏳ Retraso de 3 segundos antes de responder
    mensaje = mensaje.lower().strip()

    # Detectar intención de conocer el producto
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
    if "muy caro" in mensaje or "precio alto" in mensaje:
        return "💰 Entiendo tu preocupación. Esta cafetera ofrece calidad profesional a un precio justo. Además, incluye *envío gratis* y garantía. ¿Quieres apartar la tuya?"

    if "por qué elegir esta" in mensaje or "comparación" in mensaje:
        return "🔍 A diferencia de otras, la *Cafetera Espresso Pro* tiene *pantalla táctil, tubo de vapor y extracción de 20 Bar*. ¿Quieres probar su calidad?"

    if "no estoy seguro" in mensaje or "quizás después" in mensaje:
        return "😊 No hay problema. ¿Qué información te ayudaría a decidirte? Puedo resolver cualquier duda."

    # Respuestas predefinidas
    for palabra_clave, respuesta in RESPUESTAS_PREDEFINIDAS.items():
        if palabra_clave in mensaje:
            iniciar_temporizador(cliente_id, enviar_mensaje_recordatorio)
            return respuesta

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
                    return f"✅ ¡Gracias {pedido['nombre']}! Tu pedido de {pedido['unidades']} unidades será enviado a {pedido['direccion']}. Te contactaremos al {pedido['telefono']}."

                return solicitar_datos_venta(cliente_id)

    iniciar_temporizador(cliente_id, enviar_mensaje_recordatorio)
    return "🤖 No estoy seguro de haber entendido. ¿Te gustaría que te ayude con algo más?"
