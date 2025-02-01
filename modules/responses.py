import json
import os
import time
import threading  # Para manejar temporizadores
from modules.producto_helper import cargar_especificaciones_producto

# Almacenar la última interacción del usuario
ULTIMA_INTERACCION = {}

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes. ¿En qué podemos ayudarte hoy?",
    "ubicacion": "📍 Estamos ubicados en Bogotá, Colombia. ¿Te gustaría saber si hacemos envíos a tu ciudad?",
    "precio": "💰 Nuestros precios varían según el producto. ¿Te gustaría conocer más detalles sobre el producto?",
}

DATOS_CLIENTE = {}

def verificar_tiempo_respuesta(cliente_id):
    """Si el cliente no responde en 5 minutos, envía un mensaje de seguimiento."""
    time.sleep(300)  # Espera 5 minutos (300 segundos)

    if cliente_id in ULTIMA_INTERACCION:
        tiempo_ultima_respuesta = ULTIMA_INTERACCION[cliente_id]
        tiempo_actual = time.time()

        if tiempo_actual - tiempo_ultima_respuesta >= 300:  # Si han pasado 5 minutos
            print(f"⏳ El cliente {cliente_id} no ha respondido en 5 minutos. Enviando mensaje de seguimiento...")
            return f"🚀 ¿Aún estás ahí? Si tienes dudas sobre la cafetera, dime y te ayudaré. 😊"

    return None

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Responde preguntas, maneja la venta y mantiene la conversación activa."""
    time.sleep(3)  # ⏳ Agregamos un retraso de 3 segundos antes de responder
    mensaje = mensaje.lower().strip()

    # Guardar el tiempo de la última interacción
    ULTIMA_INTERACCION[cliente_id] = time.time()

    # Iniciar temporizador de seguimiento
    threading.Thread(target=verificar_tiempo_respuesta, args=(cliente_id,)).start()

    # Detectar intención de obtener especificaciones del producto
    if "especificaciones" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]
        
        respuesta = f"🔦 *{producto['nombre']}* 🔦\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "¿Te gustaría recibirla en tu domicilio con pago contra entrega? 😊"
        
        return respuesta

    # Buscar respuestas predefinidas
    for palabra_clave, respuesta in RESPUESTAS_PREDEFINIDAS.items():
        if palabra_clave in mensaje:
            return respuesta + "\n\n¿Necesitas más información sobre la cafetera?"

    # Proceso de venta: solicitar datos del cliente
    if "quiero comprar" in mensaje or "cómo lo adquiero" in mensaje:
        return solicitar_datos_venta(cliente_id)
    
    # Capturar información del cliente sin reiniciar la conversación
    if cliente_id not in DATOS_CLIENTE:
        DATOS_CLIENTE[cliente_id] = {}

    datos_faltantes = ["nombre", "direccion", "telefono", "unidades"]
    
    for key in datos_faltantes:
        if key not in DATOS_CLIENTE[cliente_id]:
            if key == "telefono" and not mensaje.isdigit():
                return "📞 El número de teléfono debe contener solo dígitos. ¿Podrías ingresarlo nuevamente?"
            
            DATOS_CLIENTE[cliente_id][key] = mensaje
            
            if all(d in DATOS_CLIENTE[cliente_id] for d in datos_faltantes):
                pedido = DATOS_CLIENTE.pop(cliente_id)  # Eliminar datos después de confirmar
                return f"✅ ¡Gracias {pedido['nombre']}! Tu pedido de {pedido['unidades']} unidades será enviado a {pedido['direccion']}. Te contactaremos al {pedido['telefono']}. 🚀"

            return solicitar_datos_venta(cliente_id)  # Seguir pidiendo datos

    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
