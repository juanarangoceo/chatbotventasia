import json
import time
from handlers.intention_classifier import clasificar_intencion
from handlers.openai_helper import generar_respuesta_ia
from handlers.user_state import obtener_estado_usuario, guardar_estado_usuario
from handlers.producto_helper import obtener_detalle_producto

# Cargar flujo de ventas
with open("flujo_ventas.json", "r", encoding="utf-8") as file:
    flujo_ventas = json.load(file)

def manejar_mensaje(mensaje, cliente_id):
    """Maneja el flujo de ventas asegurando que OpenAI siempre responda correctamente."""
    
    estado_actual = obtener_estado_usuario(cliente_id) or {"estado": "inicio"}
    intencion = clasificar_intencion(mensaje.lower())

    print(f"🟢 Estado actual: {estado_actual['estado']} | 🎯 Intención detectada: {intencion}")

    # 🔹 Respuesta inteligente con OpenAI si es necesario
    if intencion not in ["comprar", "datos", "confirmar"]:
        return generar_respuesta_ia(mensaje)

    # 🔹 Si el cliente dice que quiere comprar
    if "comprar" in mensaje.lower() or mensaje.lower() in ["sí", "si", "quiero"]:
        guardar_estado_usuario(cliente_id, "recopilar_datos")
        return "🎉 ¡Excelente! Para enviarte la *Cafetera Espresso Pro* con *pago contra entrega*, necesito estos datos:\n1️⃣ *Nombre:*\n2️⃣ *Teléfono:*\n3️⃣ *Dirección:*\n4️⃣ *Ciudad:*\n✍️ Envíalos en este formato para procesar tu pedido."

    # 🔹 Si el cliente envía los datos
    elif estado_actual["estado"] == "recopilar_datos":
        datos = extraer_datos(mensaje)
        if datos:
            guardar_estado_usuario(cliente_id, "verificar_datos", **datos)
            return f"✅ ¡Perfecto! Estos son tus datos:\n📌 *Nombre:* {datos['nombre']}\n📌 *Teléfono:* {datos['telefono']}\n📌 *Dirección:* {datos['direccion']}\n📌 *Ciudad:* {datos['ciudad']}\n\n¿Son correctos? Responde *Sí* o indícame si hay algún error. ✍️"
        else:
            return "⚠️ No entendí bien tus datos. Envíalos en este formato: *Nombre, Teléfono, Dirección, Ciudad*."

    # 🔹 Confirmar los datos
    elif estado_actual["estado"] == "verificar_datos":
        if mensaje.lower() in ["sí", "si", "correcto", "confirmo"]:
            guardar_estado_usuario(cliente_id, "finalizar")
            return "🎉 ¡Listo! Tu pedido ha sido confirmado. 📦 Pronto recibirás la *Cafetera Espresso Pro* en tu dirección. ¡Gracias por confiar en nosotros! ☕"
        else:
            guardar_estado_usuario(cliente_id, "recopilar_datos")
            return "Por favor, envíanos nuevamente los datos corregidos. 📋"

    return generar_respuesta_ia(mensaje)
