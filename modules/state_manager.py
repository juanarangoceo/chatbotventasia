import time

usuarios_estado = {}

def obtener_estado_usuario(cliente_id):
    """Obtiene el estado actual del usuario. Si no existe, inicia en 'inicio'."""
    if cliente_id not in usuarios_estado:
        usuarios_estado[cliente_id] = {"estado": "inicio", "timestamp": time.time()}

    print(f"🟢 Estado actual de {cliente_id}: {usuarios_estado[cliente_id]['estado']}")  # DEBUG
    return usuarios_estado[cliente_id]["estado"]

def actualizar_estado_usuario(cliente_id, nuevo_estado):
    """Actualiza el estado del usuario en la conversación y lo imprime para depuración."""
    usuarios_estado[cliente_id] = {"estado": nuevo_estado, "timestamp": time.time()}
    print(f"🔄 Estado actualizado: {cliente_id} -> {nuevo_estado}")  # DEBUG
