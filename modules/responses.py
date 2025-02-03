import json
import os
import time
from modules.producto_helper import cargar_especificaciones_producto

# Diccionario para guardar la información de cada usuario
usuarios = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona la respuesta y el flujo de ventas de manera estructurada."""
    
    time.sleep(2)  # ⏳ Simula un tiempo de respuesta
    mensaje = mensaje.lower().strip()

    # Si el cliente es nuevo, inicia el flujo con un saludo
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte con la *Cafetera Espresso Pro*. \n📍 *¿Desde qué ciudad nos escribes?*"

    estado = usuarios[cliente_id]["estado"]

    # Preguntar la ciudad si es el primer mensaje
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return f"¡Gracias! Enviamos a {usuarios[cliente_id]['ciudad']} con *pago contra entrega* 🚚.\n¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*?"

    # Manejar preguntas sobre el producto
    if any(x in mensaje for x in ["características", "detalles", "qué incluye", "precio"]):
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return producto["error"]

        respuesta = f"📌 *{producto['nombre']}* 📌\n{producto['descripcion']}\n\n"
        respuesta += "🔹 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚛 {producto['envio']}\n\n"
        respuesta += "¿Te gustaría que te ayudemos a realizar tu compra? 😊"

        usuarios[cliente_id]["estado"] = "preguntar_compra"
        return respuesta

    # Manejo de objeciones (ejemplo: precio)
    if "caro" in mensaje:
        return "💰 Entiendo tu preocupación sobre el precio. Sin embargo, la *Cafetera Espresso Pro* es una inversión a largo plazo. Te ahorrará dinero en café de cafetería. ¿Quieres proceder con la compra?"

    # Preguntar si desea realizar la compra
    if estado == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "recopilar_datos"
        return "📦 ¡Genial! Para completar tu compra, por favor indícame:\n1️⃣ *Nombre y apellido*\n2️⃣ *Teléfono* 📞\n3️⃣ *Dirección* 🏡\n4️⃣ *Ciudad* 🏙️"

    # Recopilar datos del cliente
    if estado == "recopilar_datos":
        usuarios[cliente_id]["datos"] = mensaje
        usuarios[cliente_id]["estado"] = "verificar_datos"
        return f"✅ *Confirmemos tu pedido:* \n{mensaje}\n\n ¿Los datos están correctos? (Responde 'Sí' para confirmar o 'No' para corregir)"

    # Confirmar el pedido
    if estado == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        usuarios[cliente_id]["estado"] = "finalizado"
        return "🎉 ¡Pedido confirmado! En las próximas horas recibirás un mensaje con la información de envío. ¡Gracias por tu compra! ☕🚀"

    # Respuesta genérica si no entiende
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
