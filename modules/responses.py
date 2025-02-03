import time
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

# Diccionario para guardar la información de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestión del flujo de ventas con respuestas más estratégicas y fluidas."""
    
    time.sleep(1)
    mensaje = mensaje.lower().strip()

    # 🟢 Iniciar flujo si el cliente es nuevo
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy *Juan*, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la *Cafetera Espresso Pro*.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    estado = usuarios[cliente_id]["estado"]

    # 🟢 Preguntar la ciudad
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return (
            f"¡Gracias! Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚.\n\n"
            "📌 *¿Quieres recibir más detalles sobre la Cafetera Espresso Pro y asegurar tu compra?* 😊"
        )

    # 🟢 Flujo de compra
    if estado in ["mostrar_info", "preguntar_compra"] and mensaje in ["sí", "si", "quiero comprar", "quiero una"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return (
            "📦 *¡Genial! Para completar tu compra, dime:*\n"
            "1️⃣ *Tu nombre completo* 👤\n"
            "2️⃣ *Número de teléfono* 📞\n"
            "3️⃣ *Dirección completa* 🏡\n"
            "4️⃣ *Ciudad* 🏙️\n\n"
            "⚠️ *Si falta algún dato, te lo recordaré antes de continuar.*"
        )

    # 🟢 Si el usuario hace preguntas mientras está en el flujo de compra
    if estado == "recopilar_datos":
        if any(x in mensaje for x in ["accesorios", "incluye", "qué trae"]):
            return (
                "🔧 *Accesorios incluidos:* \n"
                "- Filtro de doble salida ☕\n"
                "- Vaporizador de leche 🥛\n"
                "- Cucharón medidor y prensador 🍵\n"
                "📦 *¡Ahora solo necesitamos tus datos para finalizar la compra!* 😊"
            )
        else:
            # Si no está preguntando sobre accesorios, validar datos
            datos = mensaje.split("\n")
            if len(datos) < 4:
                return (
                    "⚠️ *Falta información.* Para continuar, envíame:\n"
                    "1️⃣ *Nombre completo* 👤\n"
                    "2️⃣ *Número de teléfono* 📞\n"
                    "3️⃣ *Dirección completa* 🏡\n"
                    "4️⃣ *Ciudad* 🏙️"
                )

            usuarios[cliente_id]["datos_pedido"] = {
                "nombre": datos[0],
                "telefono": datos[1],
                "direccion": datos[2],
                "ciudad": datos[3]
            }
            usuarios[cliente_id]["estado"] = "verificar_datos"
            return (
                f"✅ *Confirmemos tu pedido:*\n"
                f"👤 *Nombre:* {datos[0]}\n"
                f"📞 *Teléfono:* {datos[1]}\n"
                f"🏡 *Dirección:* {datos[2]}\n"
                f"🏙️ *Ciudad:* {datos[3]}\n\n"
                "📦 *¿Los datos están correctos?* (Responde *Sí* para confirmar o *No* para corregir)"
            )

    # 🟢 Confirmar pedido con cierre de venta
    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return "🎉 *¡Pedido confirmado!* En breve recibirás detalles sobre la entrega. ¡Gracias por tu compra! ☕🚀"

    # 🔴 Responder cualquier otra pregunta sin perder el enfoque en la venta
    return generar_respuesta_ia(
        f"El usuario preguntó: {mensaje}. Responde en *una frase corta* y destaca un *beneficio clave* de la *Cafetera Espresso Pro*. "
        "Luego, haz una pregunta estratégica para avanzar en la compra."
    )
