import time
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

# Diccionario para guardar la información de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas con respuestas estructuradas usando IA."""
    
    time.sleep(1)  # Simula un tiempo de respuesta
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
            "📌 ¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*?"
        )

    # 🟢 Si el usuario menciona "características", "precio" o "detalles", responder con OpenAI y vender
    if any(x in mensaje for x in ["características", "precio", "detalles", "cómo funciona", "incluye"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return generar_respuesta_ia(
            f"Responde de manera amigable y breve. Explica en menos de 3 frases las características de {producto['nombre']}."
            " Luego, pregunta al cliente si le gustaría comprar con envío gratis y pago contra entrega."
        )

    # 🟢 Manejo de objeción de precio
    if "cara" in mensaje or "muy costosa" in mensaje:
        return generar_respuesta_ia(
            "El cliente dice que el precio es alto. Responde destacando el valor, calidad y ahorro a largo plazo."
            " Luego, pregunta si quiere que le ayudes a procesar el pedido con pago contra entrega."
        )

    # 🟢 Si el usuario muestra interés en comprar, pedir datos
    if "comprar" in mensaje or "quiero una" in mensaje:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        usuarios[cliente_id]["datos_pedido"] = {}
        return (
            "📦 ¡Genial! Para completar tu compra, por favor dime:\n"
            "1️⃣ *Tu nombre completo* \n"
            "2️⃣ *Número de teléfono* 📞 \n"
            "3️⃣ *Dirección completa* 🏡 \n"
            "4️⃣ *Ciudad* 🏙️"
        )

    # 🟢 Recopilar datos del cliente
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
            f"👤 Nombre: {datos[0]}\n"
            f"📞 Teléfono: {datos[1]}\n"
            f"🏡 Dirección: {datos[2]}\n"
            f"🏙️ Ciudad: {datos[3]}\n\n"
            "📝 ¿Los datos están correctos? (Responde *Sí* para confirmar o *No* para corregir)"
        )

    # 🟢 Confirmar pedido final
    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return "🎉 ¡Pedido confirmado! Te contactaremos pronto con los detalles de entrega. ☕🚀"

    # 🔴 Si no entiende la pregunta, responder con OpenAI y seguir vendiendo
    return generar_respuesta_ia(
        f"El usuario preguntó: {mensaje}. Responde de manera corta y natural, "
        "asegurándote de guiar la conversación hacia la venta de la *Cafetera Espresso Pro*."
    )
