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
            f"📌 ¿Te gustaría conocer más sobre nuestra *{producto['nombre']}*?"
        )

    # 🟢 Manejar preguntas sobre características del producto
    if any(x in mensaje for x in ["características", "detalles", "qué incluye"]):
        respuesta = (
            f"📌 *{producto['nombre']}* 📌\n"
            f"📝 {producto['descripcion']}\n\n"
            "🔹 *Características principales:* \n"
            + "\n".join([f"- {c}" for c in producto["caracteristicas"]]) +
            f"\n💰 *Precio:* {producto['precio']}\n"
            f"🚛 {producto['envio']}\n\n"
            "📦 ¿Te gustaría que te ayudemos a realizar tu compra? 😊"
        )

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return respuesta

    # 🟢 Responder sobre el precio específico del producto
    if any(x in mensaje for x in ["precio", "cuánto cuesta", "valor"]):
        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return (
            f"💰 El precio de la *{producto['nombre']}* es de *{producto['precio']}*.\n\n"
            "🚛 *Envío gratis* a toda Colombia con *pago contra entrega*.\n\n"
            "📦 ¿Quieres que te ayude a procesar tu pedido?"
        )

    # 🟢 Manejo de objeción de precio
    if any(x in mensaje for x in ["cara", "muy costosa", "descuento"]):
        return (
            "💰 Entiendo tu preocupación sobre el precio.\n\n"
            f"Pero la *{producto['nombre']}* es una inversión de calidad ☕✨.\n\n"
            "Con su sistema de presión de 15 bares y su diseño fácil de usar, "
            "te permitirá preparar café de nivel profesional en casa y ahorrar dinero en cafeterías.\n\n"
            "📦 ¿Te gustaría que te ayudemos a realizar tu compra?"
        )

    # 🟢 Confirmar compra y solicitar datos
    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        usuarios[cliente_id]["datos"] = {}  # Inicializa el diccionario de datos
        return (
            "📦 *¡Genial! Para completar tu compra, dime:*\n"
            "1️⃣ *Nombre y apellido* 😊\n"
            "2️⃣ *Teléfono* 📞\n"
            "3️⃣ *Dirección completa* 🏡\n"
            "4️⃣ *Ciudad* 🏙️"
        )

    # 🟢 Recopilar datos del cliente y verificar si están completos
    if estado == "recopilar_datos":
        datos = mensaje.split("\n")
        detalles_cliente = usuarios[cliente_id]["datos"]

        for dato in datos:
            if "nombre" in dato.lower():
                detalles_cliente["nombre"] = dato.split(":")[-1].strip()
            elif "teléfono" in dato.lower() or "telefono" in dato.lower():
                detalles_cliente["telefono"] = dato.split(":")[-1].strip()
            elif "dirección" in dato.lower() or "direccion" in dato.lower():
                detalles_cliente["direccion"] = dato.split(":")[-1].strip()
            elif "ciudad" in dato.lower():
                detalles_cliente["ciudad"] = dato.split(":")[-1].strip()

        # Verificar si algún campo está vacío
        campos_faltantes = [campo for campo in ["nombre", "telefono", "direccion", "ciudad"] if campo not in detalles_cliente]

        if campos_faltantes:
            return (
                f"⚠️ *Falta información.* Por favor, envíame:\n"
                + "\n".join([f"🔹 {c.capitalize()}" for c in campos_faltantes])
            )

        # Guardar los datos
        usuarios[cliente_id]["estado"] = "verificar_datos"

        return (
            "✅ *Confirmemos tu pedido:*\n"
            f"👤 *Nombre:* {detalles_cliente['nombre']}\n"
            f"📞 *Teléfono:* {detalles_cliente['telefono']}\n"
            f"🏡 *Dirección:* {detalles_cliente['direccion']}\n"
            f"🏙️ *Ciudad:* {detalles_cliente['ciudad']}\n\n"
            "📝 ¿Los datos están correctos? (Responde 'Sí' para confirmar o 'No' para corregir)"
        )

    # 🟢 Permitir corrección de datos
    if estado == "verificar_datos" and mensaje.lower() in ["no", "corregir", "cambiar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return "Por favor, envíame nuevamente tus datos corregidos siguiendo el mismo formato. 😊"

    # 🟢 Confirmar pedido final
    if estado == "verificar_datos" and mensaje.lower() in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return (
            "🎉 *¡Pedido confirmado!*\n\n"
            "En las próximas horas recibirás un mensaje con la información de envío.\n\n"
            "📦 Gracias por tu compra y disfruta tu *Cafetera Espresso Pro* ☕🚀."
        )

    # 🔴 Respuesta genérica si no entiende
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
