from utils.database import conectar_db

def guardar_estado_usuario(cliente_id, estado, ciudad=None, nombre=None, telefono=None, direccion=None):
    """Guarda o actualiza el estado de un usuario en la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO usuarios (cliente_id, estado, ciudad, nombre, telefono, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(cliente_id) DO UPDATE SET 
        estado=excluded.estado, ciudad=excluded.ciudad, 
        nombre=excluded.nombre, telefono=excluded.telefono, 
        direccion=excluded.direccion
    """, (cliente_id, estado, ciudad, nombre, telefono, direccion))
    
    conn.commit()
    conn.close()

def obtener_estado_usuario(cliente_id):
    """Recupera el estado de un usuario desde la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT estado, ciudad, nombre, telefono, direccion FROM usuarios WHERE cliente_id = ?", (cliente_id,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        return {
            "estado": usuario[0],
            "ciudad": usuario[1],
            "nombre": usuario[2],
            "telefono": usuario[3],
            "direccion": usuario[4]
        }
    return None

def borrar_estado_usuario(cliente_id):
    """Elimina el estado de un usuario de la base de datos cuando finaliza la conversación."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM usuarios WHERE cliente_id = ?", (cliente_id,))
    
    conn.commit()
    conn.close()
