from collections import defaultdict
import time

# Diccionario para manejar el estado del usuario
usuarios = defaultdict(lambda: {"estado": "inicio", "ultimo_mensaje": time.time()})

def actualizar_estado(cliente_id, nuevo_estado):
    """Actualiza el estado de la conversación del usuario."""
    usuarios[cliente_id]["estado"] = nuevo_estado
    usuarios[cliente_id]["ultimo_mensaje"] = time.time()

def obtener_estado(cliente_id):
    """Devuelve el estado actual del usuario."""
    return usuarios[cliente_id]["estado"]

def inactividad_cliente(cliente_id, tiempo_maximo=300):
    """Verifica si un usuario ha estado inactivo por más de `tiempo_maximo` segundos."""
    tiempo_actual = time.time()
    return (tiempo_actual - usuarios[cliente_id]["ultimo_mensaje"]) > tiempo_maximo
