import time
from modules.producto_helper import cargar_especificaciones_producto
from modules.openai_helper import generar_respuesta_ia

usuarios = {}

def formatear_respuesta(texto):
    """Aplica formato a la respuesta: negritas, emojis y preguntas finales."""
    palabras_clave = ["precio", "descuento", "envío", "calidad", "garantía", "oferta"]
    for palabra in palabras_clave:
        texto = texto.replace(palabra, f"*{palabra}*")
    
    if not texto.endswith("?"):
        texto += " 😊"

    return texto

def obtener_respuesta_predefinida(mensaje, cliente_id):
    """Gestiona el flujo de ventas y usa OpenAI si es necesario."""
    time.sleep(1)
    mensaje = mensaje.lower().strip()

    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad", "historial": ""}
        return "¡Hola! ☕ Soy *Juan*, tu asesor de café. ¿Desde qué ciudad nos escribes?"

    estado = usuarios[cliente_id]["estado"]
    historial = usuarios[cliente_id]["historial"]

    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["ciudad"] = mensaje.capitalize()
        usuarios[cliente_id]["estado"] = "mostrar_info"
        return f"¡Gracias! Enviamos a *{mensaje.capitalize()}* con *pago contra entrega* 🚚. ¿Quieres conocer más sobre la *{producto['nombre']}*?"

    if any(x in mensaje for x in ["precio", "cuánto cuesta"]):
        return f"💰 El precio de la *{producto['nombre']}* es *{producto['precio']}*. 🚛 *Envío gratis*. ¿Quieres que te ayude con tu pedido?"

    respuesta_ia = generar_respuesta_ia(mensaje, historial)
    usuarios[cliente_id]["historial"] += f"\nCliente: {mensaje}\nJuan: {respuesta_ia}\n"

    return formatear_respuesta(respuesta_ia)
