from collections import defaultdict

# Diccionario para manejar el flujo de ventas
sesiones = defaultdict(lambda: {"paso": 1, "datos": {}})

def flujo_ventas(usuario, mensaje):
    """Gestiona la conversación siguiendo un guion de ventas estructurado."""
    paso = sesiones[usuario]["paso"]
    datos = sesiones[usuario]["datos"]

    if paso == 1:
        sesiones[usuario]["paso"] = 2
        return "¡Hola! Soy Sandra, tu asesora de ventas. ¿Te gustaría conocer nuestros precios y promociones?"

    elif paso == 2:
        sesiones[usuario]["paso"] = 3
        return (
            "Tenemos las siguientes opciones:\n"
            "🔦 1 Linterna Kit - $89.900 🚚\n"
            "🔦 2 Linternas Kit - $159.900 🚚\n\n"
            "📌 ¿Para qué la necesitas? Te puedo ayudar a elegir la mejor opción. 😊"
        )

    elif paso == 3:
        sesiones[usuario]["paso"] = 4
        return (
            "¡Excelente elección! Esta linterna con herramientas es ideal para emergencias o uso diario. 🔦\n"
            "¿Te gustaría que te la enviemos con pago contra entrega? 🚛💨"
        )

    elif paso == 4:
        sesiones[usuario]["paso"] = 5
        return "Perfecto. Para completar tu pedido, necesito tus datos: \n📍 *Nombre, Teléfono, Ciudad y Dirección*."

    elif paso == 5:
        # Verifica si el cliente ha proporcionado los datos requeridos
        claves_faltantes = ["nombre", "telefono", "ciudad", "direccion"]
        for clave in claves_faltantes:
            if clave not in datos:
                datos[clave] = mensaje  # Guardar el dato proporcionado
                if clave == "nombre":
                    return "¡Gracias! Ahora dime tu número de teléfono 📞."
                elif clave == "telefono":
                    return "Perfecto. ¿En qué ciudad te encuentras? 🏙️"
                elif clave == "ciudad":
                    return "¡Casi terminamos! Ahora, necesito la dirección exacta para el envío. 📦"

        sesiones[usuario]["paso"] = 6  # Marca el flujo como completado
        return f"¡Genial {datos['nombre']}! 🎉 Tu pedido se ha registrado con éxito. Te contactaremos al {datos['telefono']} para coordinar el envío. ¡Gracias por tu compra! 🛍️"

    return "No entendí bien. ¿Podrías repetirlo?"

