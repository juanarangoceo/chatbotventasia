import time

# Diccionario de usuarios para rastrear su estado en la conversación
usuarios = {}

def actualizar_estado(cliente_id, nuevo_estado):
    """Actualiza el estado del cliente en la conversación."""
    if cliente_id not in usuarios:
        usuarios[cliente_id] = {"estado": nuevo_estado, "ultimo_mensaje": time.time()}
    else:
        usuarios[cliente_id]["estado"] = nuevo_estado
        usuarios[cliente_id]["ultimo_mensaje"] = time.time()

def obtener_estado(cliente_id):
    """Obtiene el estado actual del cliente."""
    return usuarios.get(cliente_id, {}).get("estado", "inicio")

def tiempo_desde_ultimo_mensaje(cliente_id):
    """Devuelve el tiempo en segundos desde el último mensaje del cliente."""
    if cliente_id in usuarios:
        return time.time() - usuarios[cliente_id]["ultimo_mensaje"]
    return float('inf')
