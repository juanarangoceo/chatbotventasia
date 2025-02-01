import json
import os
import time
import threading
from datetime import datetime, timedelta
from modules.producto_helper import cargar_especificaciones_producto  

PRODUCTO_JSON_PATH = os.path.join(os.getcwd(), "producto.json")

DATOS_CLIENTE = {}
ULTIMA_INTERACCION = {}  # Para rastrear el tiempo de la última respuesta
PASO_CLIENTE = {}  # Para seguir el estado de la conversación del cliente

GANCHOS = [
    "💡 ¿Tienes alguna duda sobre el producto? Estoy aquí para ayudarte.",
    "📦 ¿Te gustaría conocer más sobre el envío y tiempo de entrega?",
    "☕ ¿Cómo te gustaría disfrutar tu café con nuestra Cafetera Espresso Pro?",
    "🚀 ¡Aprovecha nuestra oferta especial! ¿Cuántas unidades necesitas?"
]

def obtener_respuesta(mensaje, cliente_id):
    """Maneja el flujo de ventas y responde de forma estratégica."""
    time.sleep(2)  # ⏳ Simulación de retraso de respuesta
    mensaje = mensaje.lower().strip()

    # Actualizamos la última interacción del usuario
    ULTIMA_INTERACCION[cliente_id] = datetime.now()

    if cliente_id not in PASO_CLIENTE:
        PASO_CLIENTE[cliente_id] = 1  # Iniciar en el primer paso

    paso = PASO_CLIENTE[cliente_id]

    if paso == 1:
        PASO_CLIENTE[cliente_id] = 2
        return "¡Hola! 😊 Soy Sandra, tu asistente. ¿Desde qué ciudad nos escribes?"

    elif paso == 2:
        PASO_CLIENTE[cliente_id] = 3
        return ("📍 Enviamos a toda Colombia con *pago contra entrega*. 🚚 Ciudades principales: 1-4 días hábiles. "
                "Poblaciones alejadas: 5-8 días. ¿Quieres conocer los precios?")

    elif paso == 3:
        PASO_CLIENTE[cliente_id] = 4
        return ("🔥 Opciones de compra:\n"
                "1️⃣ *1 Cafetera Espresso Pro* – *$399,900 COP* 🚚\n"
                "2️⃣ *2 Cafeteras Espresso Pro* – *$749,900 COP* 🚚\n"
                "📦 Envío GRATIS a toda Colombia.\n"
                "¿Para qué tipo de café la necesitas? ☕")

    elif paso == 4:
        PASO_CLIENTE[cliente_id] = 5
        return ("✨ Esta cafetera es ideal para espresso, capuchino y café con leche. "
                "Tiene *pantalla táctil*, *vaporizador de leche* y *presión profesional*.\n"
                "👉 ¿Te gustaría recibirla con *pago contra entrega*?")

    elif paso == 5:
        PASO_CLIENTE[cliente_id] = 6
        return ("¡Genial! Para procesar tu pedido, necesito estos datos:\n"
                "1️⃣ Nombre 😊\n"
                "2️⃣ Teléfono 📞\n"
                "3️⃣ Ciudad 🏙\n"
                "4️⃣ Dirección 🏡\n"
                "5️⃣ Cantidad de cafeteras 📦")

    elif paso == 6:
        # Guardamos los datos del cliente
        if cliente_id not in DATOS_CLIENTE:
            DATOS_CLIENTE[cliente_id] = {}

        if "teléfono" not in DATOS_CLIENTE[cliente_id] and mensaje.isdigit():
            DATOS_CLIENTE[cliente_id]["teléfono"] = mensaje
            return "📞 Gracias. Ahora dime tu *ciudad*."

        if "ciudad" not in DATOS_CLIENTE[cliente_id]:
            DATOS_CLIENTE[cliente_id]["ciudad"] = mensaje
            return "📍 ¿Cuál es tu dirección exacta para el envío? 🏡"

        if "dirección" not in DATOS_CLIENTE[cliente_id]:
            DATOS_CLIENTE[cliente_id]["dirección"] = mensaje
            return "📦 ¿Cuántas cafeteras deseas pedir? (1 o 2)"

        if "cantidad" not in DATOS_CLIENTE[cliente_id] and mensaje.isdigit():
            DATOS_CLIENTE[cliente_id]["cantidad"] = mensaje
            pedido = DATOS_CLIENTE.pop(cliente_id)
            return (f"✅ ¡Gracias! Tu pedido de *{pedido['cantidad']}* Cafetera(s) será enviado a:\n"
                    f"🏠 {pedido['dirección']}, {pedido['ciudad']}.\n"
                    f"📞 Te contactaremos al {pedido['teléfono']} para confirmar.\n"
                    "🚚 *Pago contra entrega*. ¡Disfruta tu café! ☕✨")

    return "🤖 ¿Tienes alguna otra pregunta antes de proceder con el pedido? 😉"


# ---------------------------
# 🔄 FUNCIONALIDAD DE GANCHO
# ---------------------------
def verificar_inactividad():
    """Verifica cada minuto si hay clientes inactivos y les envía un mensaje gancho."""
    while True:
        time.sleep(60)  # Revisión cada 60 segundos
        ahora = datetime.now()
        for cliente_id, ultima_interaccion in list(ULTIMA_INTERACCION.items()):
            if ahora - ultima_interaccion > timedelta(minutes=5):  # Si pasaron 5 min sin respuesta
                mensaje_gancho = GANCHOS[hash(cliente_id) % len(GANCHOS)]  # Mensaje aleatorio
                enviar_mensaje(cliente_id, mensaje_gancho)  # Simulación de envío
                del ULTIMA_INTERACCION[cliente_id]  # Eliminamos para evitar envíos repetidos

def enviar_mensaje(cliente_id, mensaje):
    """Simula el envío de un mensaje de seguimiento."""
    print(f"📢 Enviando mensaje a {cliente_id}: {mensaje}")

# Iniciar el verificador en segundo plano
hilo_verificador = threading.Thread(target=verificar_inactividad, daemon=True)
hilo_verificador.start()
