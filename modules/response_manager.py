from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto
from modules.verificacion_datos import verificar_datos
from modules.state_manager import obtener_estado_usuario, actualizar_estado_usuario

def manejar_mensaje(mensaje, cliente_id, intencion=None):
    """Genera la respuesta adecuada en función de la intención del usuario."""
    
    if intencion is None:
        intencion = clasificar_intencion(mensaje)
    
    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    # Diccionario de respuestas
    respuestas = {
        "saludo": f"¡Hola! ☕ Soy *Juan*, tu asesor de café. ¿Cómo puedo ayudarte con la *{producto['nombre']}* hoy?",
        "cafetera": f"¡Hola! ☕ Soy *Juan*, tu asesor experto en café. \n\n📍 *¿Desde qué ciudad nos escribes?*",
        "precio": f"💰 El precio de la *{producto['nombre']}* es de *{producto['precio']}*. 🚛 Envío gratis a toda Colombia.",
        "caracteristicas": f"🔍 *Características principales:* \n" + "\n".join([f"- {c}" for c in producto["caracteristicas"]]),
        "compra": "📦 Para completar tu compra, dime: \n1️⃣ *Nombre y apellido* \n2️⃣ *Teléfono* \n3️⃣ *Dirección completa* \n4️⃣ *Ciudad*",
        "envio": "🚛 Hacemos envíos gratis a toda Colombia con *pago contra entrega*.",
        "confirmacion": "🎉 ¡Pedido confirmado! Gracias por tu compra. ☕🚀",
        "despedida": "¡Gracias por tu tiempo! Que tengas un excelente día. 😊",
        "desconocido": "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles?"
    }

    # Si el usuario menciona "cafetera", actualizar el estado
    if intencion == "cafetera":
        actualizar_estado_usuario(cliente_id, "preguntar_ciudad")

    return respuestas.get(intencion, respuestas["desconocido"])
