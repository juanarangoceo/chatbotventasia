import re
import json
from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto
from modules.state_manager import obtener_estado_usuario, actualizar_estado_usuario
from modules.openai_helper import generar_respuesta_ia

# Cargar flujo de ventas desde flujo_ventas.json
with open("flujo_ventas.json", "r", encoding="utf-8") as file:
    flujo_ventas = json.load(file)

usuarios_info = {}

# Expresión regular para detectar si un mensaje parece una ciudad
CIUDAD_REGEX = r"^[a-zA-ZÀ-ÿ\s]+$"

def manejar_mensaje(mensaje, cliente_id, intencion=None):
    """Genera la respuesta adecuada en función de la intención del usuario y el estado del flujo."""
    
    if intencion is None:
        intencion = clasificar_intencion(mensaje)
    
    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    estado_actual = obtener_estado_usuario(cliente_id)

    # 🟢 Inicio del chatbot
    if estado_actual == "inicio" or intencion == "saludo":
        actualizar_estado_usuario(cliente_id, "preguntar_ciudad")
        return flujo_ventas["inicio"]

    # 🟢 Recibir la ciudad y avanzar en el flujo de ventas con OpenAI
    elif estado_actual == "preguntar_ciudad":
        if cliente_id in usuarios_info and "ciudad" in usuarios_info[cliente_id]:
            return f"📍 Ya registramos tu ciudad: {usuarios_info[cliente_id]['ciudad']}. {flujo_ventas['preguntar_ciudad']}"

        # **Validar si el mensaje parece ser una ciudad**
        if not re.match(CIUDAD_REGEX, mensaje):
            return "⚠️ Por favor, ingresa una ciudad válida para continuar."

        usuarios_info[cliente_id] = {"ciudad": mensaje.capitalize()}
        actualizar_estado_usuario(cliente_id, "mostrar_info")

        print(f"✅ Ciudad recibida: {mensaje.capitalize()}")  # DEBUG
        print(f"🔄 Estado actualizado a: mostrar_info")  # DEBUG

        # **Llamar a OpenAI después de recibir la ciudad**
        respuesta_ia = generar_respuesta_ia(f"El cliente es de {mensaje.capitalize()}, ¿qué podemos ofrecerle?", "")
        print(f"📡 Respuesta de OpenAI: {respuesta_ia}")  # DEBUG

        return (
            flujo_ventas["preguntar_ciudad"].format(ciudad=mensaje.capitalize()) + "\n\n" +
            f"📌 {respuesta_ia}"
        )

    # 🟢 Mostrar información del producto
    elif estado_actual == "mostrar_info":
        actualizar_estado_usuario(cliente_id, "preguntar_precio")
        return flujo_ventas["mostrar_info"]

    return "🤖 No estoy seguro de haber entendido, pero dime, ¿qué te gustaría saber sobre la cafetera? ☕"
