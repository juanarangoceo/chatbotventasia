import json
import os
import time  
from modules.producto_helper import cargar_especificaciones_producto  
from modules.config_loader import cargar_prompt  # Cargar el prompt estructurado

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

# Diccionario para manejar la conversación de cada usuario
CONVERSACIONES = {}

# Cargar el prompt de ventas desde prompt.json
PROMPT_VENTAS = cargar_prompt()

# Mensaje de bienvenida cuando es la primera interacción del usuario
MENSAJE_BIENVENIDA = """¡Hola! ☕ Soy Juan, tu asesor de café profesional. 
Estoy aquí para ayudarte a descubrir cómo puedes disfrutar en casa de un café digno de cafetería, con nuestra Máquina para Café Automática. 🙌
✍️ Cuéntanos, *¿Desde qué ciudad nos escribes?* 🏙️"""

DATOS_CLIENTE = {}

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona la conversación y activa el flujo de ventas tras recibir la ciudad del cliente."""
    time.sleep(3)  # ⏳ Simulación de respuesta natural

    mensaje = mensaje.lower().strip()
    
    # Verificar si el cliente ya ha interactuado antes
    if cliente_id not in CONVERSACIONES:
        CONVERSACIONES[cliente_id] = {"estado": "esperando_ciudad"}
        return MENSAJE_BIENVENIDA

    # Si el chatbot está esperando la ciudad, guardarla y activar el flujo de ventas
    if CONVERSACIONES[cliente_id]["estado"] == "esperando_ciudad":
        CONVERSACIONES[cliente_id]["estado"] = "flujo_ventas"
        return (
            f"¡Gracias! 📍 Verificaremos si tenemos envío a *{mensaje.capitalize()}*.\n\n"
            f"{PROMPT_VENTAS['guion_ventas']['interaccion_1']}\n"
        )

    # Flujo de ventas apegado al prompt
    return continuar_flujo_ventas(mensaje, cliente_id)

def continuar_flujo_ventas(mensaje, cliente_id):
    """Sigue el guion de ventas estructurado en el prompt."""
    estado = CONVERSACIONES[cliente_id].get("estado", "")

    if estado == "flujo_ventas":
        if "precio" in mensaje or "cuánto cuesta" in mensaje:
            CONVERSACIONES[cliente_id]["estado"] = "detalles_producto"
            return f"{PROMPT_VENTAS['guion_ventas']['interaccion_2']}\n"

        elif "uso" in mensaje:
            CONVERSACIONES[cliente_id]["estado"] = "confirmar_envio"
            return f"{PROMPT_VENTAS['guion_ventas']['interaccion_3']}\n"

        elif "quiero comprar" in mensaje or "envíamelo" in mensaje:
            CONVERSACIONES[cliente_id]["estado"] = "solicitar_datos"
            return (
                f"{PROMPT_VENTAS['guion_ventas']['interaccion_4']}\n"
                "Por favor, envíanos estos datos para procesar tu compra:\n"
                "1️⃣ Nombre y apellido\n"
                "2️⃣ Teléfono 📞\n"
                "3️⃣ Dirección de envío 🏡\n"
                "4️⃣ Ciudad 🏙️\n"
            )

    elif estado == "solicitar_datos":
        if all(x in mensaje for x in ["nombre", "teléfono", "dirección"]):
            CONVERSACIONES[cliente_id]["estado"] = "confirmar_pedido"
            return f"{PROMPT_VENTAS['guion_ventas']['interaccion_5']}\n"

    return "🤖 No estoy seguro de haber entendido. ¿Podrías darme más detalles o reformular tu pregunta?"
