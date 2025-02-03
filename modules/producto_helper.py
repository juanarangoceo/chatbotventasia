import json

def cargar_especificaciones_producto():
    """Carga los detalles del producto desde un archivo JSON."""
    try:
        with open("producto.json", "r", encoding="utf-8") as file:
            producto = json.load(file)
        return producto
    except Exception as e:
        return {"error": f"❌ Error al cargar el producto: {str(e)}"}
