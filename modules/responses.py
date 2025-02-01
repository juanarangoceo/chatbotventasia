import json
import os
import time  
from modules.producto_helper import cargar_especificaciones_producto  

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

RESPUESTAS_PREDEFINIDAS = {
    "horario": "📅 Atendemos de 9 AM a 6 PM, de lunes a viernes. ¿En qué te puedo ayudar?",
    "ubicacion": "📍 Estamos en Bogotá, Colombia. Hacemos envíos a todo el país. ¿Desde dónde nos escribes?",
    "precio": "💰 El precio varía según el modelo. ¿Te gustaría conocer los detalles del producto?",
}

DATOS_CLIENTE = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Maneja la conversación para responder preguntas y concretar la venta."""
    time.sleep(2)  # ⏳ Agregamos un retraso de 2 segundos antes de responder
    mensaje = mensaje.lower().strip()
    
    # Si el cliente pregunta por el producto, dar detalles resumidos
    if "especificaciones" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]
        
        respuesta = (
            f"🔹 *{producto['nombre']}* 🔹\n"
            f"{producto['descripcion']}\n\n"
            "📌 *Características principales:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]]) +
            f"\n💰 *Precio:* {producto['precio']}\n🚛 {producto['envio']}\n\n"
            "👉 ¿Te gustaría comprarlo? 😊"
        )
        
        return respuesta

    # Responder preguntas predefinidas
    for palabra_clave, respuesta in RESPUESTAS_PREDEFINIDAS.items():
        if palabra_clave in mensaje:
            return respuesta

    # Iniciar el proceso de compra
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
                    pedido = DATOS_CLIENTE.pop(cliente_id)
                    return f"✅ ¡Gracias {pedido['nombre']}! Tu pedido de {pedido['unidades']} unidades será enviado a {pedido['direccion']}. Te contactaremos al {pedido['telefono']}."

                return solicitar_datos_venta(cliente_id)  # Seguir pidiendo datos

    # Manejo de objeciones y dudas antes de cerrar la venta
    return "🤖 ¿Tienes alguna otra pregunta antes de proceder con el pedido?"
