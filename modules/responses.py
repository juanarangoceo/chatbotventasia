import json
import os
import time  
from modules.producto_helper import cargar_especificaciones_producto  

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes. ¿En qué podemos ayudarte hoy?",
    "ubicacion": "📍 Estamos ubicados en Bogotá, Colombia. ¿Te gustaría saber si hacemos envíos a tu ciudad?",
    "precio": "💰 Nuestros precios varían según el producto. ¿Te gustaría conocer más detalles sobre el producto?",
}

DATOS_CLIENTE = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Revisa si el mensaje coincide con una respuesta predefinida y maneja la venta."""
    time.sleep(3)  # ⏳ Agregamos un retraso de 3 segundos antes de responder
    mensaje = mensaje.lower().strip()
    
    # Detectar intención de obtener especificaciones del producto
    if "especificaciones" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]
        
        respuesta = f"🔦 *{producto['nombre']}* 🔦\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "¿Te gustaría adquirirlo? 😊"
        
        return respuesta

    # Buscar respuestas predefinidas
    for palabra_clave, respuesta in RESPUESTAS_PREDEFINIDAS.items():
        if palabra_clave in mensaje:
            return respuesta

    # Proceso de venta: solicitar datos del cliente
    if "quiero comprar" in mensaje or "cómo lo adquiero" in mensaje:
        return solicitar_datos_venta(cliente_id)
    
    # Capturar información del cliente y validar datos
    if cliente_id in DATOS_CLIENTE:
        datos_faltantes = ["nombre", "direccion", "telefono", "unidades"]
        for key in datos_faltantes:
            if key not in DATOS_CLIENTE[cliente_id]:
                # Validar número de teléfono
                if key == "telefono" and not mensaje.isdigit():
                    return "📞 El número de teléfono debe contener solo dígitos. ¿Podrías ingresarlo nuevamente?"
                
                DATOS_CLIENTE[cliente_id][key] = mensaje
                
                # Si se completan todos los datos, confirmar el pedido
                if all(d in DATOS_CLIENTE[cliente_id] for d in datos_faltantes):
                    pedido = DATOS_CLIENTE.pop(cliente_id)  # Eliminar datos después de confirmar
                    return f"✅ ¡Gracias {pedido['nombre']}! Tu pedido de {pedido['unidades']} unidades será enviado a {pedido['direccion']}. Te contactaremos al {pedido['telefono']}."
                
                return solicitar_datos_venta(cliente_id)  # Seguir pidiendo datos

    # Mejorar respuesta por defecto para preguntas no reconocidas
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
