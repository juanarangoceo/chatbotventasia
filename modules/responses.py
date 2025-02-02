import time
from modules.openai_helper import generar_respuesta_ia

# Diccionario para rastrear el estado del cliente
usuarios = {}

def obtener_respuesta(mensaje, cliente_id):
    """Gestiona la conversación estructurada para vender la cafetera Espresso Pro."""
    
    time.sleep(2)  # ⏳ Simula un tiempo de respuesta natural
    mensaje = mensaje.lower().strip()

    # 🔹 Si el cliente menciona "cafetera", iniciar el flujo de ventas
    if "cafetera" in mensaje:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad"}
        return "¡Hola! ☕ Soy Juan, tu asesor de café profesional. Estoy aquí para ayudarte a descubrir cómo puedes disfrutar en casa de un café digno de cafetería, con nuestra *Cafetera Espresso Pro*.\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"

    # 🔹 Si el cliente responde con la ciudad, iniciar el flujo de ventas
    if cliente_id in usuarios and usuarios[cliente_id]["estado"] == "preguntar_ciudad":
        usuarios[cliente_id]["estado"] = "flujo_ventas"
        return generar_respuesta_ia(f"El cliente escribe desde {mensaje}. Inicia la venta de la Cafetera Espresso Pro con preguntas concretas para cerrar la compra.")

    # 🔹 Si el cliente ya está en el flujo de ventas, seguir con OpenAI
    return generar_respuesta_ia(mensaje)
