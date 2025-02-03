import json
import time
from modules.state_manager import obtener_estado, actualizar_estado
from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto

# Cargar información del producto
producto = cargar_especificaciones_producto()

# Función principal para manejar respuestas
def manejar_respuesta(mensaje, cliente_id):
    """Gestiona el flujo de ventas y procesa respuestas dinámicamente."""

    mensaje = mensaje.lower().strip()
    estado_actual = obtener_estado(cliente_id)

    # 🟢 Iniciar conversación
    if estado_actual is None:
        actualizar_estado(cliente_id, "preguntar_ciudad")
        return f"¡Hola! ☕ Soy *Juan*, tu asesor de café profesional. \n\n📍 *¿Desde qué ciudad nos escribes?*"

    # 🟢 Manejar flujo de ventas
    if estado_actual == "preguntar_ciudad":
        actualizar_estado(cliente_id, "mostrar_info", {"ciudad": mensaje})
        return f"¡Gracias! Enviamos a *{mensaje.capitalize()}* con *pago contra entrega* 🚚. \n\n📌 ¿Te gustaría conocer más sobre nuestra *{producto['nombre']}*?"

    if estado_actual == "mostrar_info" and mensaje in ["sí", "si", "claro"]:
        actualizar_estado(cliente_id, "preguntar_compra")
        return f"🔹 *Características principales de {producto['nombre']}:* \n" + "\n".join([f"- {c}" for c in producto["caracteristicas"]]) + "\n\n💰 *Precio:* {producto['precio']} \n📦 ¿Quieres hacer tu pedido?"

    if estado_actual == "preguntar_compra" and mensaje in ["sí", "si", "quiero comprar"]:
        actualizar_estado(cliente_id, "recopilar_datos")
        return "📦 *¡Genial! Para completar tu compra, dime:\n1️⃣ *Nombre y apellido* 😊\n2️⃣ *Teléfono* 📞\n3️⃣ *Dirección completa* 🏡\n4️⃣ *Ciudad* 🏙️"

    if estado_actual == "recopilar_datos":
        datos_usuario = extraer_datos(mensaje)
        if not datos_usuario:
            return "⚠️ *Falta información.* Por favor, envíame:\n🔹 Nombre\n🔹 Teléfono\n🔹 Dirección\n🔹 Ciudad"
        
        actualizar_estado(cliente_id, "verificar_datos", datos_usuario)
        return f"✅ *Confirmemos tu pedido:*\n👤 *Nombre:* {datos_usuario['nombre']}\n📞 *Teléfono:* {datos_usuario['telefono']}\n🏡 *Dirección:* {datos_usuario['direccion']}\n🏙️ *Ciudad:* {datos_usuario['ciudad']}\n\n📝 ¿Está todo correcto? (Responde 'Sí' para confirmar o 'No' para corregir)"

    if estado_actual == "verificar_datos" and mensaje in ["sí", "si", "correcto"]:
        actualizar_estado(cliente_id, "finalizado")
        return "🎉 *¡Pedido confirmado!* En las próximas horas recibirás información sobre tu envío. 📦☕ ¡Gracias por tu compra!"

    # 🟢 Enviar preguntas genéricas a ChatGPT
    return clasificar_intencion(mensaje)

# Función auxiliar para extraer datos del mensaje
def extraer_datos(mensaje):
    datos = mensaje.split("\n")
    detalles = {}

    for dato in datos:
        if "nombre" in dato.lower():
            detalles["nombre"] = dato.split(":")[-1].strip()
        elif "teléfono" in dato.lower():
            detalles["telefono"] = dato.split(":")[-1].strip()
        elif "dirección" in dato.lower():
            detalles["direccion"] = dato.split(":")[-1].strip()
        elif "ciudad" in dato.lower():
            detalles["ciudad"] = dato.split(":")[-1].strip()

    return detalles if len(detalles) == 4 else None
