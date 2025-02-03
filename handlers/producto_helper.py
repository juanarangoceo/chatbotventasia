import json

# Cargar el JSON una sola vez en memoria
try:
    with open("producto.json", "r", encoding="utf-8") as file:
        PRODUCTO = json.load(file)
except Exception as e:
    PRODUCTO = {"error": f"❌ Error al cargar el producto: {str(e)}"}

def cargar_especificaciones_producto():
    """Retorna todas las especificaciones del producto."""
    return PRODUCTO

def obtener_detalle_producto(campo):
    """Obtiene un campo específico del JSON del producto."""
    return PRODUCTO.get(campo, f"⚠️ El detalle '{campo}' no está disponible.")
