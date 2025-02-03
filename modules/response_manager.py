from modules.intention_classifier import clasificar_intencion
from modules.producto_helper import cargar_especificaciones_producto
from modules.state_manager import obtener_estado_usuario, actualizar_estado_usuario

usuarios_info = {}

def manejar_mensaje(mensaje, cliente_id, intencion=None):
    """Genera la respuesta adecuada en función de la intención del usuario y el estado del flujo."""
    
    if intencion is None:
        intencion = clasificar_intencion(mensaje)
    
    producto = cargar_especificaciones_producto()
    if "error" in producto:
        return producto["error"]

    estado_actual = obtener_estado_usuario(cliente_id)

    # 🟢 Inicio del chatbot
    if estado_actual == "inicio" or intencion == "saludo":
        actualizar_estado_usuario(cliente_id, "preguntar_ciudad")
        return "¡Hola! ☕ Soy *Juan*, tu asesor experto en café. 📍 *¿Desde qué ciudad nos escribes?*"

    # 🟢 Guardar la ciudad y avanzar
    elif estado_actual == "preguntar_ciudad":
        usuarios_info[cliente_id] = {"ciudad": mensaje.capitalize()}
        actualizar_estado_usuario(cliente_id, "mostrar_info")
        return (
            f"¡Gracias! Enviamos a *{mensaje.capitalize()}* con *pago contra entrega* 🚚.\n\n"
            f"📌 La *{producto['nombre']}* ofrece café de calidad barista en casa. ¿Te gustaría conocer más detalles?"
        )

    return "🤖 No estoy seguro de haber entendido, pero dime, ¿qué te gustaría saber sobre la cafetera? ☕"
