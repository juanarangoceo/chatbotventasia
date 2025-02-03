import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from modules.responses import manejar_mensaje

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Chatbot de Ventas con IA está activo."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    print(f"📩 Mensaje recibido de {sender}: {incoming_msg}")

    response_text = manejar_mensaje(incoming_msg, sender)

    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
