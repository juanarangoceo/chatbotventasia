usuarios_estado = {}

def obtener_estado_usuario(cliente_id):
    return usuarios_estado.get(cliente_id, "inicio")

def actualizar_estado_usuario(cliente_id, nuevo_estado):
    usuarios_estado[cliente_id] = nuevo_estado
