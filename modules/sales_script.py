from collections import defaultdict

# Diccionario para manejar el flujo de ventas
sesiones = defaultdict(lambda: {"paso": 1})

def flujo_ventas(usuario, mensaje):
    """Gestiona la conversación siguiendo el guion de ventas en 5 pasos."""
    paso = sesiones[usuario]["paso"]

    if paso == 1:
        sesiones[usuario]["paso"] = 2
        return "¡Hola! Soy Sandra. ¿Te gustaría conocer nuestros precios?"

    elif paso == 2:
        sesiones[usuario]["paso"] = 3
        return "Aquí están nuestros paquetes:\n1️⃣ 1 Linterna Kit - $89.900 🚚\n2️⃣ 2 Linternas Kit - $159.900 🚚\n¿Para qué la necesitas?"

    elif paso == 3:
        sesiones[usuario]["paso"] = 4
        return "¡Buena elección! Esta linterna con herramientas es ideal para emergencias. ¿Quieres que te la enviemos con pago contra entrega?"

    elif paso == 4:
        sesiones[usuario]["paso"] = 5
        return "Perfecto! Dime tus datos de envío: Nombre, Teléfono, Ciudad y Dirección."

    elif paso == 5:
        return "¡Todo confirmado! 🎉 Gracias por tu compra."

    return None
