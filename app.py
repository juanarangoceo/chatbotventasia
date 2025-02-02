import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from modules.flow_manager import actualizar_estado, obtener_estado, inactividad_cliente
from modules.responses import obtener_respuesta
from modules.openai_helper import generar_respuesta_ia

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Chatbot de ventas activo."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    """Maneja los mensajes de WhatsApp y responde con OpenAI si es necesario."""
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From", "")

    print(f"📩 Mensaje recibido de {sender}: {incoming_msg}")

    # Verificar si el usuario está inactivo y enviar mensaje gancho
    if inactividad_cliente(sender, 300):
        return str(MessagingResponse().message("¿Sigues ahí? 😊 Estoy aquí para ayudarte con la Cafetera Espresso Pro."))

    # Obtener respuesta basada en el flujo
    respuesta = obtener_respuesta(incoming_msg, sender)

    # Si no hay respuesta del flujo, usar OpenAI para responder preguntas abiertas
    if not respuesta:
        respuesta = generar_respuesta_ia(incoming_msg)

    # Enviar respuesta a WhatsApp
    resp = MessagingResponse()
    resp.message(respuesta)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
