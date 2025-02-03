import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from modules.responses import obtener_respuesta_predefinida  # Se asegura que sea el nombre correcto

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Chatbot de Ventas con IA está activo."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        sender = request.values.get("From", "")

        if not incoming_msg:
            return str(MessagingResponse().message("⚠️ No recibí un mensaje válido. Inténtalo nuevamente."))

        print(f"📩 Mensaje recibido de {sender}: {incoming_msg}")

        # Generar respuesta con el flujo optimizado
        response_text = obtener_respuesta_predefinida(incoming_msg, sender)

        print(f"🤖 Respuesta generada: {response_text}")

        resp = MessagingResponse()
        resp.message(response_text)

        return str(resp)

    except Exception as e:
        print(f"❌ ERROR en procesamiento del mensaje: {str(e)}")
        return str(MessagingResponse().message("⚠️ Ocurrió un error inesperado. Inténtalo de nuevo más tarde."))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
