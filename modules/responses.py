RESPUESTAS_PREDEFINIDAS = {
    "horario": "Nuestro horario de atención es de 9 AM a 6 PM, de lunes a viernes.",
    "ubicacion": "Estamos ubicados en Bogotá, Colombia.",
    "precio": "Nuestros precios varían según el producto. ¿Cuál te interesa?",
}

def obtener_respuesta_predefinida(mensaje):
    """Revisa si el mensaje coincide con una respuesta predefinida."""
    mensaje = mensaje.lower()
    for palabra_clave, respuesta in RESPUESTAS_PREDEFINIDAS.items():
        if palabra_clave in mensaje:
            return respuesta
    return None
