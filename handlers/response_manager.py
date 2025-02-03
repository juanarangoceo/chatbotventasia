import json
import time
from handlers.intention_classifier import clasificar_intencion
from handlers.openai_helper import generar_respuesta_ia
from handlers.user_state import obtener_estado_usuario, guardar_estado_usuario

# Cargar flujo de ventas
with open("flujo_ventas.json", "r", encoding="utf-8") as file:
    flujo_ventas = json.load(file)

def manejar_mensaje(mensaje, cliente_id):
    """Maneja el flujo de ventas y la conversación con el usuario de forma fluida."""
    
    estado_actual = obtener_estado_usuario(cliente_id) or {"estado": "inicio"}
    intencion = clasificar_intencion(mensaje)

    print(f"🟢 Estado actual del usuario: {estado_actual['estado']} | 🎯 Intención detectada: {intencion}")

    # 🟢 Manejo de interrupciones (el usuario pregunta algo fuera de orden)
    if intencion in ["precio", "caracteristicas", "envio", "credito", "colores", "molino"]:
        return generar_respuesta_ia(mensaje)

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

def extraer_datos(mensaje):
    """Extrae los datos del usuario desde un mensaje desordenado."""
    import re
    datos = {}

    nombre_match = re.search(r"nombre[:\-]?\s*([a-zA-Z\s]+)", mensaje, re.IGNORECASE)
    telefono_match = re.search(r"tel[eé]fono[:\-]?\s*(\d{7,10})", mensaje, re.IGNORECASE)
    direccion_match = re.search(r"direcci[oó]n[:\-]?\s*([\w\s,.-]+)", mensaje, re.IGNORECASE)
    ciudad_match = re.search(r"ciudad[:\-]?\s*([a-zA-Z\s]+)", mensaje, re.IGNORECASE)

    if nombre_match:
        datos["nombre"] = nombre_match.group(1).strip()
    if telefono_match:
        datos["telefono"] = telefono_match.group(1).strip()
    if direccion_match:
        datos["direccion"] = direccion_match.group(1).strip()
    if ciudad_match:
        datos["ciudad"] = ciudad_match.group(1).strip()

    return datos if len(datos) >= 3 else None
