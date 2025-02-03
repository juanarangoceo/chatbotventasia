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
    """Maneja el flujo de ventas asegurando respuestas cortas y dirigidas a la compra."""
    
    estado_actual = obtener_estado_usuario(cliente_id) or {"estado": "inicio"}
    intencion = clasificar_intencion(mensaje)

    print(f"🟢 Estado actual: {estado_actual['estado']} | 🎯 Intención detectada: {intencion}")

    # 🟢 Manejo de interrupciones (preguntas fuera de orden)
    if intencion in ["precio", "caracteristicas", "envio", "credito", "colores", "molino"]:
        return responder_informacion(intencion)

    # 🟢 Inicio del chatbot
    if estado_actual["estado"] == "inicio":
        guardar_estado_usuario(cliente_id, "preguntar_ciudad")
        return flujo_ventas["inicio"]

    # 🟢 Usuario responde con la ciudad
    elif estado_actual["estado"] == "preguntar_ciudad":
        if not mensaje.replace(" ", "").isalpha():
            return "⚠️ La ciudad ingresada no es válida. ¿Desde qué ciudad nos escribes? 📍"
        
        guardar_estado_usuario(cliente_id, "mostrar_info", ciudad=mensaje.capitalize())
        time.sleep(2)
        return flujo_ventas["preguntar_ciudad"].format(ciudad=mensaje.capitalize())

    # 🟢 Mostrar información del producto
    elif estado_actual["estado"] == "mostrar_info":
        guardar_estado_usuario(cliente_id, "preguntar_precio")
        time.sleep(2)
        return flujo_ventas["mostrar_info"]

    # 🟢 Preguntar precio
    elif estado_actual["estado"] == "preguntar_precio":
        guardar_estado_usuario(cliente_id, "preguntar_compra")
        time.sleep(2)
        return flujo_ventas["preguntar_precio"]

    # 🟢 Preguntar si desea comprar
    elif estado_actual["estado"] == "preguntar_compra":
        if mensaje.lower() in ["sí", "si", "quiero", "me interesa", "ok"]:
            guardar_estado_usuario(cliente_id, "recopilar_datos")
            time.sleep(2)
            return flujo_ventas["preguntar_compra"]
        else:
            return "📌 Entiendo, dime si necesitas más detalles. ¿Te gustaría saber más sobre la cafetera? ☕"

    # 🟢 Recopilar datos del usuario
    elif estado_actual["estado"] == "recopilar_datos":
        datos = extraer_datos(mensaje)
        if datos:
            guardar_estado_usuario(cliente_id, "verificar_datos", **datos)
            return flujo_ventas["recopilar_datos"]
        else:
            return "⚠️ No entendí bien tus datos. Por favor, envíalos en el formato correcto."

    # 🟢 Verificar datos del usuario
    elif estado_actual["estado"] == "verificar_datos":
        if mensaje.lower() in ["sí", "si", "correcto", "confirmo"]:
            guardar_estado_usuario(cliente_id, "finalizar")
            time.sleep(2)
            return flujo_ventas["finalizar"]
        else:
            guardar_estado_usuario(cliente_id, "recopilar_datos")
            return "Por favor, envíanos nuevamente los datos corregidos. 📋"

    return "🤖 No entendí bien. ¿En qué te puedo ayudar con la cafetera? ☕"

def responder_informacion(intencion):
    """Genera respuestas optimizadas para cada tipo de pregunta manteniendo el flujo de ventas."""
    respuestas = {
        "precio": "💰 *Precio:* $420,000 COP con *envío GRATIS* 🚚. ¿Quieres que te la enviemos con *pago contra entrega*? 📦",
        "caracteristicas": "🔹 *Cafetera Espresso Pro* ☕\n- *15 bares de presión* 🔥\n- *Espumador de leche integrado* 🥛\n- *Compatible con café molido* 🌱\n- *Depósito de agua de 1.6L* 💧\n\n📦 ¿Quieres recibirla con *pago contra entrega*?",
        "envio": "🚛 *Hacemos envíos a toda Colombia.* \n📍 *Ciudades principales:* 1-4 días hábiles. \n🏡 *Poblaciones alejadas:* 5-8 días hábiles.\n\n📦 ¿Quieres recibirla con *pago contra entrega*?",
        "credito": "💳 Puedes pagarla a crédito con *Addi*. Solo ingresa aquí y selecciona la opción de pago: [🔗 Enlace de pago]",
        "colores": "🎨 Actualmente solo está disponible en *Negro con Plateado* 🖤⚙️. ¿Te gustaría recibir la tuya?",
        "molino": "⚙️ La *Cafetera Espresso Pro* *no tiene molino incorporado*. Funciona con café molido. ¿Te gustaría recibir la tuya con *pago contra entrega*? 🚛📦"
    }
    return respuestas.get(intencion, "🤖 Lo siento, no entendí bien. ¿Puedes reformular tu pregunta? ☕")

