import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from modules.openai_helper import generar_respuesta_ia

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar API Key de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("❌ ERROR: No se encontró la API Key en las variables de entorno")
    exit(1)

print(f"✅ API Key detectada correctamente: {openai_api_key[:5]}...")

# Inicializar Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Chatbot de Ventas con IA está activo."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    """Recibe mensajes de WhatsApp y responde con OpenAI."""
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    print(f"📩 Mensaje recibido de {sender}: {incoming_msg}")

    # Generar respuesta de OpenAI
    response_text = generar_respuesta_ia(incoming_msg)

    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
