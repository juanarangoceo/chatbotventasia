import re

def clasificar_intencion(mensaje):
    """Clasifica la intención del mensaje del usuario."""
    mensaje = mensaje.lower().strip()

    patrones = {
        "saludo": [r"hola", r"buenos días", r"buenas tardes", r"hey", r"qué tal", r"cómo estás"],
        "cafetera": [r"cafetera", r"quiero una cafetera", r"máquina de café", r"espresso pro", r"quiero comprar cafetera"],
        "precio": [r"cuánto cuesta", r"precio", r"valor"],
        "caracteristicas": [r"qué incluye", r"detalles", r"especificaciones", r"características"],
        "compra": [r"quiero comprar", r"cómo comprar", r"ordenar", r"adquirir"],
        "envio": [r"envío", r"cómo me llega", r"tiempo de entrega"],
        "confirmacion": [r"es correcto", r"confirmo", r"todo bien"],
        "ubicacion": [r"dónde están", r"puedo ver la cafetera", r"tienen tienda"],
        "colores": [r"qué colores tienen", r"colores disponibles"],
        "credito": [r"se puede pagar a crédito", r"tienen financiamiento"],
        "molino": [r"tiene molino", r"muele café"]
    }

    for intencion, lista_patrones in patrones.items():
        for patron in lista_patrones:
            if re.search(patron, mensaje):
                return intencion

    return "desconocido" 
