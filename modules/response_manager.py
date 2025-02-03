from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto
from modules.verificacion_datos import verificar_datos

def manejar_mensaje(mensaje, cliente_id, intencion=None):
    """Genera la respuesta adecuada en función de la intención del usuario."""
    
    if intencion is None:
        intencion = clasificar_intencion(mensaje)
    
    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]
    
    respuestas = {
        "saludo": f"¡Hola! ☕ Soy *Juan*, tu asesor de café. ¿Cómo puedo ayudarte con la *{producto['nombre']}* hoy?",
        "precio": f"💰 El precio de la *{producto['nombre']}* es de *{producto['precio']}*.",
        "caracteristicas": f"🔍 *Características principales:* \n" + "\n".join([f"- {c}" for c in producto["caracteristicas"]]),
        "compra": "📦 Para completar tu compra, dime: \n1️⃣ *Nombre y apellido* \n2️⃣ *Teléfono* \n3️⃣ *Dirección completa* \n4️⃣ *Ciudad*",
        "envio": "🚛 Hacemos envíos gratis a toda Colombia con *pago contra entrega*.",
        "confirmacion": "🎉 ¡Pedido confirmado! Gracias por tu compra. ☕🚀",
        "despedida": "¡Gracias por tu tiempo! Que tengas un excelente día. 😊",
        "desconocido": "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles?"
    }
    
    return respuestas.get(intencion, respuestas["desconocido"])
