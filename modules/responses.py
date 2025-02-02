import time
import json
from modules.producto_helper import cargar_especificaciones_producto

# Almacena el estado de los clientes
usuarios = {}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la conversación y sigue el flujo de ventas correctamente."""
    
    time.sleep(2)  # Simula un tiempo de respuesta
    
    mensaje = mensaje.lower().strip()

    # 🔹 Si el usuario es nuevo, iniciar la conversación con el saludo correcto
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return (
            "¡Hola! ☕ Soy Juan, tu asesor de café profesional. "
            "Estoy aquí para ayudarte con la *Cafetera Espresso Pro*. 🙌\n\n"
            "✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
        )

    # 🔹 Si está en la fase de preguntar la ciudad, guardar y avanzar
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.title()  # Guardar la ciudad con mayúscula inicial
        usuarios[cliente_id]["estado"] = "confirmar_interes"
        return (
            f"¡Gracias! Enviamos a {mensaje.title()} con *pago contra entrega* 🚛.\n\n"
            "¿Te gustaría conocer más sobre nuestra *Cafetera Espresso Pro*? ☕"
        )

    # 🔹 Si el usuario confirma que quiere saber más
    if usuarios[cliente_id]["estado"] == "confirmar_interes" and mensaje in ["sí", "si", "claro", "me gustaría saber más"]:
        usuarios[cliente_id]["estado"] = "explicar_beneficios"
        return (
            "Perfecto! Nuestra *Cafetera Espresso Pro* ☕ tiene:\n"
            "- Presión de 15 bares para un espresso perfecto\n"
            "- Espumador de leche integrado 🥛\n"
            "- Preparación automática con un solo toque 🔘\n\n"
            "👉 *¿Prefieres café espresso o cappuccino?*"
        )

    # 🔹 Si el usuario pregunta por las características del producto
    if "características" in mensaje or "detalles" in mensaje or "qué incluye" in mensaje:
        producto = cargar_especificaciones_producto()
        if "error" in producto:
            return "⚠️ Lo siento, hubo un error al cargar la información del producto."

        respuesta = f"📦 *{producto['nombre']}* ☕\n{producto['descripcion']}\n\n"
        respuesta += "📌 *Características:* \n"
        respuesta += "\n".join([f"- {c}" for c in producto["caracteristicas"]])
        respuesta += f"\n💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
        respuesta += "👉 *¿Quieres que te ayude a procesar tu pedido?* 📦"

        return respuesta

    # 🔹 Si el usuario responde sobre el tipo de café, pasar al cierre
    if usuarios[cliente_id]["estado"] == "explicar_beneficios":
        usuarios[cliente_id]["estado"] = "cierre_venta"
        return (
            "¡Excelente elección! 🎉 Con nuestra *Cafetera Espresso Pro*, "
            "podrás preparar tu café favorito con calidad de cafetería en casa. ☕🏡\n\n"
            "📦 *¿Te gustaría que te la enviemos con pago contra entrega?* 🚛💨"
        )

    # 🔹 Si el usuario confirma la compra, pedir datos para el envío
    if usuarios[cliente_id]["estado"] == "cierre_venta" and mensaje in ["sí", "si", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "solicitar_datos"
        return (
            "¡Genial! Para completar tu pedido, necesito algunos datos: \n"
            "📍 *Nombre, Teléfono, Ciudad y Dirección*."
        )

    # 🔹 Si el usuario proporciona datos, confirmar el pedido
    if usuarios[cliente_id]["estado"] == "solicitar_datos":
        usuarios[cliente_id]["estado"] = "pedido_confirmado"
        return (
            "✅ ¡Gracias! Tu pedido ha sido registrado con éxito. "
            "Te contactaremos pronto para confirmar la entrega. 📦🚛"
        )

    # 🔹 Respuesta por defecto si el mensaje no encaja en el flujo
    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles?"
