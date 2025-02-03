usuarios_estado = {}

def obtener_estado_usuario(cliente_id):
    """Obtiene el estado actual del usuario. Si no existe, inicia en 'inicio'."""
    estado = usuarios_estado.get(cliente_id, "inicio")
    print(f"🟢 Estado actual de {cliente_id}: {estado}")  # Debug log
    return estado

def actualizar_estado_usuario(cliente_id, nuevo_estado):
    """Actualiza el estado del usuario en la conversación y lo imprime para depuración."""
    print(f"🔄 Actualizando estado de {cliente_id}: {nuevo_estado}")  # Debug log
    usuarios_estado[cliente_id] = nuevo_estado
