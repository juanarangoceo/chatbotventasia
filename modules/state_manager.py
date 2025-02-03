import time

usuarios_estado = {}

def obtener_estado_usuario(cliente_id):
    """Obtiene el estado actual del usuario. Si no existe, inicia en 'inicio'."""
    estado_info = usuarios_estado.get(cliente_id, {"estado": "inicio", "timestamp": time.time()})
    
    # Si el usuario lleva más de 10 minutos sin interactuar, reiniciar su estado
    if time.time() - estado_info["timestamp"] > 600:
        estado_info = {"estado": "inicio", "timestamp": time.time()}
    
    print(f"🟢 Estado actual de {cliente_id}: {estado_info['estado']}")  # DEBUG
    return estado_info["estado"]

def actualizar_estado_usuario(cliente_id, nuevo_estado):
    """Actualiza el estado del usuario en la conversación y lo imprime para depuración."""
    usuarios_estado[cliente_id] = {"estado": nuevo_estado, "timestamp": time.time()}
    print(f"🔄 Estado actualizado: {cliente_id} -> {nuevo_estado}")  # DEBUG
