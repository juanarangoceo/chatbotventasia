import json
import os
import time
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

# Almacena los clientes para controlar la primera interacción
usuarios = {}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la respuesta y el flujo de ventas de manera estructurada."""
    
    time.sleep(3)  # ⏳ Simula un tiempo de respuesta
    
    mensaje = mensaje.lower().strip()

    # 🔹 Saludo y pregunta inicial si es un nuevo usuario
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte a descubrir cómo puedes disfrutar en casa de un café digno de cafetería, con nuestra Máquina para Café Automática. 🙌\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"
    
    # 🔹 Si el usuario ya respondió con una ciudad, activar el flujo de ventas
    if usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["estado"] = "flujo_ventas"
        return generar_respuesta_ia(mensaje)  # Aquí se invoca OpenAI

    # 🔹 Si ya está en el flujo de ventas, responder con IA
    return generar_respuesta_ia(mensaje)
