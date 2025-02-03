import time
from modules.producto_helper import cargar_especificaciones_producto

usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas con respuestas estructuradas basadas en el producto."""

    time.sleep(1)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy *Juan*, tu asesor de café profesional.\n\n"
            f"Estoy aquí para ayudarte con la *{producto['nombre']}*.\n\n"
            "📍 *¿Desde qué ciudad nos escribes?*"
        )

    estado = usuarios[cliente_id]["estado"]

    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return (
            f"¡Gracias! Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚.\n\n"
            f"📌 ¿Te gustaría conocer más sobre nuestra *{producto['nombre']}*?"
        )

    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return (
            "📦 *¡Genial! Para completar tu compra, dime:*\n"
            "1️⃣ *Nombre completo* 😊\n"
            "2️⃣ *Teléfono* 📞\n"
            "3️⃣ *Dirección completa* 🏡\n"
            "4️⃣ *Ciudad* 🏙️"
        )

    if estado == "recopilar_datos":
        datos = mensaje.split("\n")
        campos_faltantes = []
        detalles_cliente = {}

        for dato in datos:
            if "nombre" in dato.lower():
                detalles_cliente["nombre"] = dato.split(":")[-1].strip()
            elif "teléfono" in dato.lower():
                detalles_cliente["telefono"] = dato.split(":")[-1].strip()
            elif "dirección" in dato.lower():
                detalles_cliente["direccion"] = dato.split(":")[-1].strip()
            elif "ciudad" in dato.lower():
                detalles_cliente["ciudad"] = dato.split(":")[-1].strip()

        for campo in ["nombre", "telefono", "direccion", "ciudad"]:
            if campo not in detalles_cliente:
                campos_faltantes.append(campo)

        if campos_faltantes:
            return f"⚠️ *Falta información.* Por favor, envíame:\n" + "\n".join([f"🔹 {c.capitalize()}" for c in campos_faltantes])

        usuarios[cliente_id]["datos"] = detalles_cliente
        usuarios[cliente_id]["estado"] = "verificar_datos"

        return (
            "✅ *Confirmemos tu pedido:*\n"
            f"👤 *Nombre:* {detalles_cliente['nombre']}\n"
            f"📞 *Teléfono:* {detalles_cliente['telefono']}\n"
            f"🏡 *Dirección:* {detalles_cliente['direccion']}\n"
            f"🏙️ *Ciudad:* {detalles_cliente['ciudad']}\n\n"
            "📝 ¿Los datos están correctos? (Responde 'Sí' para confirmar o 'No' para corregir)"
        )
