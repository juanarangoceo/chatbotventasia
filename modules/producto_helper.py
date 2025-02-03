import json

def cargar_especificaciones_producto():
    try:
        with open("producto.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        return {"error": f"❌ Error al cargar la información del producto: {str(e)}"}
