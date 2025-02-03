usuarios_estado = {}

def obtener_estado_usuario(cliente_id):
    """Obtiene el estado actual del usuario. Si no existe, inicia en 'inicio'."""
    return usuarios_estado.get(cliente_id, "inicio")

def actualizar_estado_usuario(cliente_id, nuevo_estado):
    """Actualiza el estado del usuario en la conversación."""
    print(f"🟢 Actualizando estado de {cliente_id} a {nuevo_estado}")  # DEBUG
    usuarios_estado[cliente_id] = nuevo_estado
