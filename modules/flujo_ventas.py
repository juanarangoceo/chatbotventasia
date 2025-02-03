from modules.producto_helper import cargar_especificaciones_producto
from modules.verificacion_datos import validar_datos_cliente

def gestionar_flujo(mensaje, cliente_id, usuarios):
    """Maneja cada etapa del flujo de ventas."""
    estado = usuarios[cliente_id]["estado"]

    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return f"📍 Enviamos a *{usuarios[cliente_id]['ciudad']}* con *pago contra entrega* 🚚. ¿Quieres conocer nuestros precios?"

    if estado == "mostrar_info":
        if mensaje in ["sí", "si", "quiero saber más"]:
            usuarios[cliente_id]["estado"] = "preguntar_compra"
            producto = cargar_especificaciones_producto()
            return (
                f"📌 *{producto['nombre']}* \n{producto['descripcion']}\n\n"
                f"💰 *Precio:* {producto['precio']}\n🚛 {producto['envio']}\n\n"
                "📦 ¿Qué uso le darás a la Máquina para Café Automática?"
            )

    if estado == "preguntar_compra":
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        usuarios[cliente_id]["datos"] = {}
        return "📦 Para continuar, dime:\n1️⃣ *Nombre* 😊\n2️⃣ *Apellido* 😊\n3️⃣ *Teléfono* 📞\n4️⃣ *Departamento* 🌄\n5️⃣ *Ciudad* 🏙\n6️⃣ *Dirección* 🏡\n7️⃣ *Color* 🎨"

    if estado == "recopilar_datos":
        faltantes = validar_datos_cliente(mensaje, cliente_id, usuarios)
        if faltantes:
            return f"⚠️ Faltan datos. Envíame:\n" + "\n".join(faltantes)

        usuarios[cliente_id]["estado"] = "verificar_datos"
        datos = usuarios[cliente_id]["datos"]
        return (
            f"✅ *Confirma tu pedido:*\n"
            f"👤 *Nombre:* {datos['nombre']}\n"
            f"📞 *Teléfono:* {datos['telefono']}\n"
            f"🏡 *Dirección:* {datos['direccion']}\n"
            f"🏙️ *Ciudad:* {datos['ciudad']}\n"
            f"🎨 *Color:* {datos['color']}\n\n"
            "📦 *¿Los datos están correctos?* (Responde *Sí* para confirmar o *No* para corregir)"
        )

    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return "🎉 *¡Pedido confirmado!* En breve recibirás detalles sobre la entrega. ¡Gracias por tu compra! ☕🚀"

    return "🤖 No entendí bien. ¿Podrías reformular tu pregunta?"
