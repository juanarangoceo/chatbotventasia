import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para manejar el estado del usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas con respuestas optimizadas y validadas."""

    time.sleep(2)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🔹 Iniciar conversación si es un nuevo usuario
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy *Juan*, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la **Cafetera Espresso Pro**.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    estado = usuarios[cliente_id]["estado"]

    # 🔹 Preguntar ciudad al inicio
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return (
            f"¡Gracias! Enviamos a **{usuarios[cliente_id]['ciudad']}** con *pago contra entrega* 🚛.\n\n"
            "📌 ¿Te gustaría conocer más sobre nuestra **Cafetera Espresso Pro**?"
        )

    # 🔹 Responder sobre características
    if any(x in mensaje for x in ["características", "detalles", "qué incluye"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = (
            f"📌 **{producto['nombre']}**\n{producto['descripcion']}\n\n"
            "🔹 **Características principales:**\n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]])
            + f"\n💰 **Precio:** {producto['precio']}\n🚛 {producto['envio']}\n\n"
            "📦 *¿Quieres que te ayude a procesar tu pedido?* 😊"
        )

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return respuesta

    # 🔹 Responder objeción de precio
    if "cara" in mensaje or "costosa" in mensaje:
        return (
            "💰 *Entiendo tu preocupación sobre el precio.*\n\n"
            "Pero la **Cafetera Espresso Pro** es una inversión que te permitirá disfrutar café de calidad "
            "en casa todos los días ☕ y ahorrar dinero en cafeterías.\n\n"
            "📦 *¿Quieres que te ayude a procesar tu pedido?*"
        )

    # 🔹 Confirmar si desea comprar
    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        usuarios[cliente_id]["datos"] = {}
        return (
            "📦 ¡Genial! Para completar tu compra, por favor dime:\n"
            "1️⃣ *Tu nombre y apellido* \n"
            "2️⃣ *Tu número de teléfono* 📞 \n"
            "3️⃣ *Tu dirección completa* 🏡 \n"
            "4️⃣ *Tu ciudad* 🏙️"
        )

    # 🔹 Recopilar datos de envío y validar
    if estado == "recopilar_datos":
        datos = usuarios[cliente_id].get("datos", {})

        if "nombre" not in datos:
            datos["nombre"] = mensaje
            return "📌 Ahora dime tu *número de teléfono* 📞"

        if "telefono" not in datos:
            datos["telefono"] = mensaje
            return "📌 Ahora dime tu *dirección completa* 🏡"

        if "direccion" not in datos:
            datos["direccion"] = mensaje
            return "📌 Finalmente, dime tu *ciudad* 🏙️"

        if "ciudad" not in datos:
            datos["ciudad"] = mensaje
            usuarios[cliente_id]["estado"] = "verificar_datos"

            return (
                f"✅ *Confirmemos tu pedido:* \n"
                f"📌 **Nombre:** {datos['nombre']}\n"
                f"📌 **Teléfono:** {datos['telefono']}\n"
                f"📌 **Dirección:** {datos['direccion']}\n"
                f"📌 **Ciudad:** {datos['ciudad']}\n\n"
                "📝 *¿Los datos están correctos? (Responde 'Sí' para confirmar o 'No' para corregir)*"
            )

    # 🔹 Confirmar y finalizar pedido
    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return (
            "🎉 **¡Pedido confirmado!**\n\n"
            "En las próximas horas recibirás un mensaje con los detalles de envío. "
            "¡Gracias por tu compra! ☕🚀"
        )

    # 🔴 Respuesta predeterminada para preguntas desconocidas
    return "🤖 No estoy seguro de haber entendido. *¿Podrías darme más detalles?*"

