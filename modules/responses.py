import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para guardar la información de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas con respuestas estructuradas basadas en el producto."""

    time.sleep(1)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🟢 Cargar información del producto
    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    # 🟢 Si el cliente es nuevo, inicia el flujo con un saludo
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy *Juan*, tu asesor de café profesional.\n\n"
            f"Estoy aquí para ayudarte con la *{producto['nombre']}*.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    estado = usuarios[cliente_id]["estado"]

    # 🟢 Preguntar la ciudad en la primera interacción
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return (
            f"¡Gracias! Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚.\n\n"
            f"📌 ¿Te gustaría conocer más sobre nuestra *{producto['nombre']}*? Responde con *Sí* o *No*."
        )

    # 🟢 Manejo de respuestas afirmativas
    if estado == "mostrar_info" and mensaje in ["sí", "si", "claro", "quiero saber más"]:
        usuarios[cliente_id]["estado"] = "mostrar_caracteristicas"
        return (
            f"✨ *{producto['nombre']}* ✨\n"
            f"📝 {producto['descripcion']}\n\n"
            "🔹 *Características principales:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]]) +
            f"\n💰 *Precio:* {producto['precio']}\n"
            f"🚛 {producto['envio']}\n\n"
            "📦 ¿Te gustaría que te ayudemos a realizar tu compra? 😊"
        )

    # 🟢 Pregunta sobre el precio
    if any(x in mensaje for x in ["precio", "cuánto cuesta", "valor"]):
        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return (
            f"💰 El precio de la *{producto['nombre']}* es de *{producto['precio']}*.\n\n"
            "🚛 *Envío gratis* a toda Colombia con *pago contra entrega*.\n\n"
            "📦 ¿Quieres que te ayude a procesar tu pedido?"
        )

    # 🟢 Confirmar compra
    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return (
            "📦 *¡Genial! Para completar tu compra, dime:*\n"
            "1️⃣ *Nombre y apellido* 😊\n"
            "2️⃣ *Teléfono* 📞\n"
            "3️⃣ *Dirección completa* 🏡\n"
            "4️⃣ *Ciudad* 🏙️"
        )

    # 🔴 Respuesta genérica si no entiende
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
