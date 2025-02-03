import json

USUARIOS_FILE = "usuarios.json"

def obtener_estado(cliente_id):
    try:
        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)
        return usuarios.get(cliente_id, {}).get("estado", None)
    except:
        return None

def actualizar_estado(cliente_id, nuevo_estado, datos=None):
    try:
        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)
    except:
        usuarios = {}

    usuarios[cliente_id] = {"estado": nuevo_estado}
    if datos:
        usuarios[cliente_id]["datos"] = datos

    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)
