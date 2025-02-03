import json
import time
from modules.producto_helper import cargar_especificaciones_producto

# Cargar datos del producto y configuraciones
with open("producto.json", "r", encoding="utf-8") as f:
    producto = json.load(f)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Cargar y guardar estados de usuarios
USUARIOS_FILE = "usuarios.json"

def cargar_usuarios():
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4)

usuarios = cargar_usuarios()

# Datos requeridos para cerrar la venta
CAMPOS_DATOS = ["nombre", "teléfono", "ciudad", "dirección"]

def obtener_respuesta(mensaje, cliente_id):
    mensaje = mensaje.lower().strip()
    time.sleep(1)  # Simulación de respuesta

    # Si el usuario es nuevo, iniciar con la pregunta de ciudad
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": "preguntar_ciudad", "datos": {}}
        guardar_usuarios(usuarios)
        return "¡Hola! ☕ Soy Juan, experto en café. Te ayudaré con la *Cafetera Espresso Pro*. 🙌\n\n✍️ *¿Desde qué ciudad nos escribes?* 🏙️"

    estado = usuarios[cliente_id]["estado"]

    # Confirmar ciudad y seguir con el proceso
    if estado == "preguntar_ciudad":
        usuarios[cliente_id]["datos"]["ciudad"] = mensaje.title()
        usuarios[cliente_id]["estado"] = "confirmar_interes"
        guardar_usuarios(usuarios)
        return f"¡Genial! Enviamos a {mensaje.title()} con *pago contra entrega* 🚛.\n\n👉 *¿Te gustaría conocer más sobre la Cafetera Espresso Pro?*"

    # Confirmar interés y dar detalles
    if estado == "confirmar_interes" and mensaje in ["sí", "si", "claro"]:
        usuarios[cliente_id]["estado"] = "explicar_beneficios"
        guardar_usuarios(usuarios)
        return (
            f"🔹 {producto['nombre']} tiene:\n"
            "- *15 bares de presión* para espressos perfectos ☕\n"
            "- *Espumador de leche* 🥛 para capuchinos cremosos\n"
            "- *Fácil de usar* con pantalla táctil\n\n"
            f"💰 *Precio:* {producto['precio']}\n🚚 {producto['envio']}\n\n"
            "✅ *¿Quieres que te la enviemos con pago contra entrega?*"
        )

    # Si el cliente quiere comprar, recolectar datos en orden
    if estado == "explicar_beneficios" and mensaje in ["sí", "quiero comprar"]:
        usuarios[cliente_id]["estado"] = "solicitar_datos"
        usuarios[cliente_id]["datos_pendientes"] = CAMPOS_DATOS.copy()
        guardar_usuarios(usuarios)
        return pedir_siguiente_dato(cliente_id)

    # Recolectar datos del cliente
    if estado == "solicitar_datos":
        campo_actual = usuarios[cliente_id]["datos_pendientes"].pop(0)
        usuarios[cliente_id]["datos"][campo_actual] = mensaje
        guardar_usuarios(usuarios)

        if usuarios[cliente_id]["datos_pendientes"]:
            return pedir_siguiente_dato(cliente_id)

        usuarios[cliente_id]["estado"] = "confirmar_datos"
        guardar_usuarios(usuarios)
        return confirmar_datos(cliente_id)

    return "🤖 No entendí bien, ¿puedes reformular tu pregunta?"

def pedir_siguiente_dato(cliente_id):
    """Solicita el siguiente dato necesario para procesar la compra."""
    campo = usuarios[cliente_id]["datos_pendientes"][0]
    preguntas = {
        "nombre": "😊 ¿Cuál es tu *nombre completo*?",
        "teléfono": "📞 ¿Cuál es tu *número de teléfono*?",
        "dirección": "🏡 ¿Cuál es la *dirección exacta* para la entrega?",
    }
    return preguntas.get(campo, "Por favor, proporciona el siguiente dato.")

def confirmar_datos(cliente_id):
    """Confirma los datos proporcionados por el cliente y cierra la venta."""
    datos = usuarios[cliente_id]["datos"]
    return (
        f"✅ *Confirmemos tu pedido:* \n"
        f"👤 *Nombre:* {datos['nombre']}\n"
        f"📞 *Teléfono:* {datos['teléfono']}\n"
        f"🏙️ *Ciudad:* {datos['ciudad']}\n"
        f"🏡 *Dirección:* {datos['dirección']}\n\n"
        "📦 *Total a pagar:* 399,900 COP al recibir.\n\n"
        "¿Todo está correcto para finalizar tu compra? 🎉"
    )
