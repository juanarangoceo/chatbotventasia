import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para manejar la información del usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas asegurando una conversación estructurada."""
    
    time.sleep(2)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🟢 Si el cliente es nuevo, inicia el flujo con un saludo
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
            "📌 ¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*? Responde 'Sí' para más detalles."
        )

    # 🟢 Mostrar información del producto si responde "sí"
    if estado == "mostrar_info" and mensaje in ["sí", "si", "quiero saber más"]:
        usuarios[cliente_id]["estado"] = "esperando_preguntas"
        producto = cargar_especificaciones_producto()
        return (
            f"📌 *{producto['nombre']}* 📌\n{producto['descripcion']}\n\n"
            "🔹 *Características:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]])
            + f"\n💰 *Precio:* {producto['precio']}\n🚛 {producto['envio']}\n\n"
            "📦 ¿Quieres realizar tu pedido ahora?"
        )

    # 🟢 Confirmar compra
    if estado == "esperando_preguntas" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return (
            "📦 ¡Genial! Para completar tu compra, por favor indícame:\n"
            "1️⃣ *Nombre y apellido* \n"
            "2️⃣ *Teléfono* 📞 \n"
            "3️⃣ *Dirección completa* 🏡 \n"
            "4️⃣ *Ciudad* 🏙️"
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

    # 🔴 Respuesta genérica si no entiende
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
