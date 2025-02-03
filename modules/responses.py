import time
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

# Diccionario para guardar la información de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas con respuestas estratégicas optimizadas."""
    
    time.sleep(1)  # Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # 🟢 Iniciar flujo de ventas con el primer mensaje
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
            "📌 ¿Quieres descubrir por qué la *Cafetera Espresso Pro* es la mejor opción para ti? 😊"
        )

    # 🟢 Responder preguntas sobre el producto con respuestas optimizadas
    if any(x in mensaje for x in ["características", "precio", "detalles", "cómo funciona", "incluye"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return generar_respuesta_ia(
            f"Explica en *dos frases* las *principales características* de la {producto['nombre']} "
            f"y cómo mejora la experiencia del café. Luego, pregunta al cliente si quiere recibirla con envío gratis."
        )

    # 🟢 Manejo de objeción de precio con cierre estratégico
    if "cara" in mensaje or "muy costosa" in mensaje:
        return generar_respuesta_ia(
            "El cliente menciona el precio. Responde con *dos frases* sobre su *calidad*, "
            "el ahorro a largo plazo y la comodidad de preparar café en casa. Luego, pregunta si quiere recibirla con pago contra entrega."
        )

    # 🟢 Si el usuario quiere comprar, pedir datos ordenadamente
    if "comprar" in mensaje or "quiero una" in mensaje:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        usuarios[cliente_id]["datos_pedido"] = {}
        return (
            "📦 ¡Genial! Para completar tu compra, dime:\n"
            "1️⃣ *Tu nombre completo* \n"
            "2️⃣ *Número de teléfono* 📞 \n"
            "3️⃣ *Dirección completa* 🏡 \n"
            "4️⃣ *Ciudad* 🏙️"
        )

    # 🟢 Recopilar datos asegurando que no falte información
    if estado == "recopilar_datos":
        datos = mensaje.split("\n")
        if len(datos) < 4:
            return (
                "⚠️ Aún faltan datos. Por favor, envíame:\n"
                "1️⃣ *Nombre y apellido* \n"
                "2️⃣ *Teléfono* 📞 \n"
                "3️⃣ *Dirección completa* 🏡 \n"
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
            f"👤 Nombre: *{datos[0]}*\n"
            f"📞 Teléfono: *{datos[1]}*\n"
            f"🏡 Dirección: *{datos[2]}*\n"
            f"🏙️ Ciudad: *{datos[3]}*\n\n"
            "📝 ¿Los datos están correctos? (Responde *Sí* para confirmar o *No* para corregir)"
        )

    # 🟢 Confirmar pedido con cierre de venta
    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return "🎉 *¡Pedido confirmado!* En breve recibirás detalles sobre la entrega. ¡Gracias por tu compra! ☕🚀"

    # 🔴 Si no entiende, responder con OpenAI de forma optimizada y seguir vendiendo
    return generar_respuesta_ia(
        f"El usuario preguntó: {mensaje}. Responde en *una frase corta* y destaca un *beneficio clave* de la *Cafetera Espresso Pro*. "
        "Luego, haz una pregunta estratégica para avanzar en la compra."
    )
