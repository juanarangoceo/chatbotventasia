import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para guardar el estado de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Maneja el flujo de conversación y ventas."""
    
    time.sleep(2)  # Simula tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🟢 Inicio del flujo de ventas
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy Juan, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la *Cafetera Espresso Pro*.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    estado = usuarios[cliente_id]["estado"]

    # 🟢 Captura de la ciudad y sigue el flujo
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return (
            f"¡Gracias! Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚.\n\n"
            "📌 ¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*?"
        )

    # 🟢 Manejo de preguntas sobre características
    if any(x in mensaje for x in ["características", "detalles", "qué incluye"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = (
            f"📌 *{producto['nombre']}* 📌\n{producto['descripcion']}\n\n"
            "🔹 *Características:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]])
            + f"\n💰 *Precio:* {producto['precio']}\n🚛 {producto['envio']}\n\n"
            "📦 ¿Te gustaría que te ayudemos a realizar tu compra? 😊"
        )

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return respuesta

    # 🟢 Manejo de objeciones de precio
    if "cara" in mensaje or "muy costosa" in mensaje:
        return (
            "💰 Entiendo tu preocupación sobre el precio. "
            "Sin embargo, la *Cafetera Espresso Pro* es una inversión a largo plazo. "
            "Te proporcionará café de alta calidad todos los días y te ahorrará dinero "
            "en cafeterías. ☕✨\n\n"
            "📦 ¿Quieres que te ayude a procesar tu pedido?"
        )

    # 🟢 Confirmar compra
    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return (
            "📦 ¡Genial! Para completar tu compra, por favor indícame:\n"
            "1️⃣ *Nombre y apellido* \n"
            "2️⃣ *Teléfono* 📞 \n"
            "3️⃣ *Dirección completa* 🏡 \n"
            "4️⃣ *Ciudad* 🏙️"
        )

    # 🟢 Validación de datos del cliente
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

    # 🔴 Respuesta genérica si no entiende
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
