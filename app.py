import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from modules.openai_helper import generar_respuesta_ia
from modules.sales_script import flujo_ventas

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

    # Seguir el flujo de ventas antes de llamar a OpenAI
    respuesta_flujo = flujo_ventas(sender, incoming_msg)
    if respuesta_flujo:
        resp = MessagingResponse()
        resp.message(respuesta_flujo)
        return str(resp)

    # Si no hay flujo de ventas, usa OpenAI
    response_text = generar_respuesta_ia(incoming_msg)

    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
