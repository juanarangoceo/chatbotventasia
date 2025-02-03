import time
from modules.flujo_ventas import gestionar_flujo
from modules.openai_helper import generar_respuesta_ia
from modules.verificacion_datos import validar_datos_cliente

# Almacenamiento de usuarios y estado
usuarios = {}

def manejar_mensaje(mensaje, cliente_id):
    """Gestiona el flujo de ventas y respuestas dinámicas."""
    time.sleep(1)
    mensaje = mensaje.lower().strip()

    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "inicio"}

    estado = usuarios[cliente_id]["estado"]

    if "cafetera" in mensaje and estado == "inicio":
        usuarios[cliente_id]["estado"] = "preguntar_ciudad"
        return "👋 ¡Hola! Soy *Juan*, tu asesor de café. ¿Desde qué ciudad nos escribes? 📍"

    if estado in ["preguntar_ciudad", "preguntar_compra", "recopilar_datos", "verificar_datos"]:
        return gestionar_flujo(mensaje, cliente_id, usuarios)

    return generar_respuesta_ia(mensaje)
