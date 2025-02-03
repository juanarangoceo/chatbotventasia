import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para almacenar información del usuario
usuarios = {}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona el flujo de ventas con respuestas estructuradas."""
    
    time.sleep(1)  # Simula tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🟢 Si el cliente menciona "cafetera", iniciar el flujo
    if "cafetera" in mensaje and cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy Juan, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la *Cafetera Espresso Pro*.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    # Si el cliente ya ha sido registrado, seguir con el flujo
    if cliente_id in usuarios:
        estado = usuarios[cliente_id]["estado"]

        if estado == "preguntar_ciudad":
            usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
            usuarios[cliente_id]["estado"] = "mostrar_info"
            return (
                f"¡Gracias! Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚.\n\n"
                "📌 ¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*?"
            )

        if estado == "mostrar_info":
            usuarios[cliente_id]["estado"] = "preguntar_compra"
            return (
                "📌 La *Cafetera Espresso Pro* es ideal para preparar café de calidad en casa. "
                "Tiene *15 bares de presión*, *espumador de leche integrado* y *diseño compacto*. ☕✨\n\n"
                "💰 *Precio:* 399,900 COP\n🚛 Envío gratis a toda Colombia con pago contra entrega.\n\n"
                "📦 ¿Te gustaría que te ayudemos a realizar tu compra?"
            )

        if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
            usuarios[cliente_id]["estado"] = "recopilar_datos"
            return (
                "📦 ¡Genial! Para completar tu compra, por favor indícame:\n"
                "1️⃣ *Nombre y apellido* \n"
                "2️⃣ *Teléfono* 📞 \n"
                "3️⃣ *Dirección completa* 🏡 \n"
                "4️⃣ *Ciudad* 🏙️"
            )

        if estado == "recopilar_datos":
            usuarios[cliente_id]["datos"] = mensaje
            usuarios[cliente_id]["estado"] = "verificar_datos"
            return (
                f"✅ *Confirmemos tu pedido:* \n{mensaje}\n\n"
                "📝 ¿Los datos están correctos? (Responde 'Sí' para confirmar o 'No' para corregir)"
            )

        if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
            usuarios[cliente_id]["estado"] = "finalizado"
            return (
                "🎉 ¡Pedido confirmado! En las próximas horas recibirás un mensaje "
                "con la información de envío. ¡Gracias por tu compra! ☕🚀"
            )

    # 🔴 Si el mensaje no encaja en ninguna parte del flujo
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
