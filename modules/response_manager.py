from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto
from modules.state_manager import obtener_estado_usuario, actualizar_estado_usuario

def manejar_mensaje(mensaje, cliente_id, intencion=None):
    """Genera la respuesta adecuada en función de la intención del usuario y el estado del flujo."""
    
    if intencion is None:
        intencion = clasificar_intencion(mensaje)
    
    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    # Obtener estado actual del usuario
    estado_actual = obtener_estado_usuario(cliente_id)

    # Flujo de ventas basado en el estado del usuario
    if estado_actual == "preguntar_ciudad":
        actualizar_estado_usuario(cliente_id, "mostrar_info")
        return (
            f"¡Gracias! Enviamos a *{mensaje.capitalize()}* con *pago contra entrega* 🚚.\n\n"
            f"📌 La *{producto['nombre']}* ofrece café de calidad barista en casa. ¿Te gustaría conocer más detalles?"
        )

    elif estado_actual == "mostrar_info":
        actualizar_estado_usuario(cliente_id, "preguntar_precio")
        return (
            f"💰 *Precio:* {producto['precio']} con *envío GRATIS* 🚛.\n\n"
            f"¿Para qué tipo de café la necesitas?"
        )

    elif estado_actual == "preguntar_precio":
        actualizar_estado_usuario(cliente_id, "preguntar_compra")
        return (
            "📦 ¿Quieres recibir la *Cafetera Espresso Pro* con pago contra entrega?"
        )

    elif estado_actual == "preguntar_compra":
        if mensaje.lower() in ["sí", "si", "quiero comprar"]:
            actualizar_estado_usuario(cliente_id, "recopilar_datos")
            return (
                "📦 *¡Genial! Para completar tu compra, dime:*\n"
                "1️⃣ *Nombre completo* 😊\n"
                "2️⃣ *Teléfono* 📞\n"
                "3️⃣ *Dirección completa* 🏡\n"
                "4️⃣ *Ciudad* 🏙️"
            )
        else:
            return "🤔 No hay problema. ¿Tienes alguna pregunta sobre la cafetera?"

    elif estado_actual == "recopilar_datos":
        actualizar_estado_usuario(cliente_id, "verificar_datos")
        return (
            "✅ *Confirmemos tu pedido:*\n"
            f"📝 Datos recibidos: {mensaje}\n\n"
            "📝 ¿Los datos son correctos? (Responde 'Sí' para confirmar o 'No' para corregir)"
        )

    elif estado_actual == "verificar_datos":
        if mensaje.lower() in ["sí", "si", "correcto"]:
            actualizar_estado_usuario(cliente_id, "finalizado")
            return (
                "🎉 *¡Pedido confirmado!*\n\n"
                "📦 En las próximas horas recibirás un mensaje con la información de envío.\n\n"
                "¡Gracias por tu compra! ☕🚀"
            )
        else:
            actualizar_estado_usuario(cliente_id, "recopilar_datos")
            return "🔄 Vamos a corregir tus datos. Envíamelos de nuevo."

    # Si el mensaje no coincide con ningún estado, se devuelve una respuesta estándar.
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles?"
