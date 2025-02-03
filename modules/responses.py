import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para manejar la información de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas asegurando que se mantenga en el embudo correctamente."""
    
    time.sleep(1.5)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🟢 Saludo inicial y solicitud de ciudad
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy Juan, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la *Cafetera Espresso Pro*.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    estado = usuarios[cliente_id]["estado"]

    # 🟢 Preguntar la ciudad en la primera interacción
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return (
            f"¡Gracias! Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚.\n\n"
            "📌 ¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*?"
        )

    # 🟢 Manejar preguntas sobre características del producto
    if any(x in mensaje for x in ["características", "detalles", "qué incluye", "especificaciones"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = (
            f"📌 *{producto['nombre']}* 📌\n{producto['descripcion']}\n\n"
            "🔹 *Características:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]])
            + f"\n💰 *Precio:* {producto['precio']}\n🚛 {producto['envio']}\n\n"
            "📦 ¿Quieres que te ayude a procesar tu pedido? 😊"
        )

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return respuesta

    # 🟢 Manejo de objeciones de precio
    if "cara" in mensaje or "muy costosa" in mensaje:
        return (
            "💰 Entiendo tu preocupación sobre el precio. "
            "Sin embargo, la *Cafetera Espresso Pro* es una inversión a largo plazo. "
            "Te permitirá disfrutar café de calidad sin gastar en cafeterías. ☕✨\n\n"
            "📦 ¿Quieres que te ayude a procesar tu pedido?"
        )

    # 🟢 Confirmar compra
    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return (
            "📦 ¡Genial! Para completar tu compra, por favor dime:\n"
            "1️⃣ *Tu nombre completo* \n"
            "2️⃣ *Tu número de teléfono* 📞 \n"
            "3️⃣ *Tu dirección completa* 🏡 \n"
            "4️⃣ *Tu ciudad* 🏙️"
        )

    # 🟢 Recopilar datos del cliente
    if estado == "recopilar_datos":
        usuarios[cliente_id]["datos"] = mensaje
        usuarios[cliente_id]["estado"] = "verificar_datos"
        return (
            f"✅ *Confirmemos tu pedido:* \n{mensaje}\n\n"
            "📝 ¿Los datos están correctos? (Responde 'Sí' para confirmar o 'No' para corregir)"
        )

    # 🟢 Confirmar pedido final
    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return (
            "🎉 ¡Pedido confirmado! En las próximas horas recibirás un mensaje "
            "con la información de envío. ¡Gracias por tu compra! ☕🚀"
        )

    # 🔴 Respuesta genérica si el mensaje no encaja en ningún flujo
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
