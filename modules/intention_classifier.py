import re

def clasificar_intencion(mensaje):
    """Clasifica la intención del mensaje del usuario."""
    mensaje = mensaje.lower().strip()

    patrones = {
        "saludo": [r"hola", r"buenos días", r"buenas tardes", r"hey"],
        "cafetera": [r"cafetera", r"quiero una cafetera", r"máquina de café"],
        "precio": [r"cu[aá]nto cuesta", r"precio", r"valor"],
        "caracteristicas": [r"qué incluye", r"detalles", r"especificaciones", r"características"],
        "compra": [r"quiero comprar", r"c[óo]mo comprar", r"ordenar", r"adquirir"],
        "envio": [r"env[íi]o", r"c[óo]mo me llega", r"tiempo de entrega"],
        "confirmacion": [r"es correcto", r"confirmo", r"todo bien"],
        "despedida": [r"gracias", r"adiós", r"nos vemos"],
    }

    for intencion, lista_patrones in patrones.items():
        for patron in lista_patrones:
            if re.search(patron, mensaje):
                return intencion

    return "desconocido"
