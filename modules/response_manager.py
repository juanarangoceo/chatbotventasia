import json
import re
import time
from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

# Diccionario para almacenar estados y datos de usuarios
usuarios_info = {}

# Flujo de ventas integrado directamente
flujo_ventas = {
    "inicio": "¡Hola! ☕ Soy *Juan*, tu asesor de café. ¿Desde qué ciudad nos escribes? 📍",
    "preguntar_ciudad": "¡Gracias! Enviamos a *{ciudad}* con *pago contra entrega* 🚛. ¿Quieres conocer el precio?",
    "mostrar_info": "La *Cafetera Espresso Pro* ofrece café de calidad barista en casa. ¿Te gustaría conocer más detalles?",
    "preguntar_precio": "💰 *Precio:* 399,900 COP con *envío GRATIS* 🚚. ¿Para qué tipo de café la necesitas?",
    "preguntar_compra": "📦 ¿Quieres recibir la *Cafetera Espresso Pro* con pago contra entrega?",
    "recopilar_datos": "Para procesar tu pedido, dime:\n\n1️⃣ *Nombre completo* 📛\n2️⃣ *Teléfono* 📞\n3️⃣ *Dirección completa* 🏡\n4️⃣ *Ciudad* 🏙️",
    "verificar_datos": "✅ *Confirmemos tu pedido:*\n\n👤 Nombre: {nombre}\n📞 Teléfono: {telefono}\n🏡 Dirección: {direccion}\n🏙️ Ciudad: {ciudad}\n\n📝 ¿Los datos son correctos? (Responde 'Sí' para confirmar o 'No' para corregir).",
    "finalizar": "🎉 ¡Pedido confirmado! Te llegará en los próximos días. ☕🚀 ¡Gracias por tu compra!"
}

def manejar_mensaje(mensaje, cliente_id, intencion=None):
    """Maneja el flujo de ventas y la conversación con el usuario."""
    
    mensaje = mensaje.strip().lower()
    estado_actual = usuarios_info.get(cliente_id, {}).get("estado", "inicio")

    print(f"🟢 Estado actual del usuario ({cliente_id}): {estado_actual}")  # DEBUG

    # 🟢 Inicio del chatbot: cualquier mensaje activa la conversación
    if estado_actual == "inicio":
        usuarios_info[cliente_id] = {"estado": "preguntar_ciudad"}
        return flujo_ventas["inicio"]

    # 🟢 Recibir la ciudad y avanzar en el flujo de ventas con OpenAI
    elif estado_actual == "preguntar_ciudad":
        if re.match(r"^[a-zA-ZÀ-ÿ\s]+$", mensaje):  # Validar que es una ciudad con letras y espacios
            usuarios_info[cliente_id]["ciudad"] = mensaje.capitalize()
            usuarios_info[cliente_id]["estado"] = "mostrar_info"

            # Llamar a OpenAI
            respuesta_ia = generar_respuesta_ia(f"El cliente es de {mensaje.capitalize()}, ¿qué podemos ofrecerle?", "")
            return flujo_ventas["preguntar_ciudad"].format(ciudad=mensaje.capitalize()) + "\n\n" + f"📌 {respuesta_ia}"
        else:
            return "⚠️ No parece ser una ciudad válida. Por favor, dime desde qué ciudad nos escribes. 📍"

    # 🟢 Mostrar información del producto
    elif estado_actual == "mostrar_info":
        usuarios_info[cliente_id]["estado"] = "preguntar_precio"
        return flujo_ventas["mostrar_info"]

    return "🤖 No estoy seguro de haber entendido, pero dime, ¿qué te gustaría saber sobre la cafetera? ☕"
