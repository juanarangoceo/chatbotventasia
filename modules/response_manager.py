from modules.responses import obtener_respuesta_predefinida
from modules.intention_classifier import clasificar_intencion

def manejar_mensaje(mensaje, cliente_id):
    """
    Gestiona el mensaje del usuario y devuelve la respuesta adecuada.
    """
    intencion = clasificar_intencion(mensaje)
    
    if intencion == "saludo":
        return "¡Hola! ☕ Soy *Juan*, tu asesor de café profesional. ¿Desde qué ciudad nos escribes?"
    
    return obtener_respuesta_predefinida(mensaje, cliente_id)
