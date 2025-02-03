import sqlite3

DB_NAME = "db.sqlite"

def conectar_db():
    """Crea la conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def inicializar_db():
    """Crea la tabla de usuarios si no existe."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT UNIQUE,
            estado TEXT,
            ciudad TEXT,
            nombre TEXT,
            telefono TEXT,
            direccion TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_estado_usuario(cliente_id, estado, ciudad=None, nombre=None, telefono=None, direccion=None):
    """Guarda o actualiza el estado de un usuario en la base de datos."""
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO usuarios (cliente_id, estado, ciudad, nombre, telefono, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(cliente_id) DO UPDATE SET 
        estado=excluded.estado, ciudad=excluded.ciudad, nombre=excluded.nombre, 
        telefono=excluded.telefono, direccion=excluded.direccion
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
