from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from handlers.response_manager import manejar_mensaje

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Chatbot de Ventas con IA activo."

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    response_text = manejar_mensaje(incoming_msg, sender)

    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
