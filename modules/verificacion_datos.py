import re

def verificar_datos(mensaje):
    """Verifica y extrae los datos del usuario para completar la compra."""
    
    datos = {}
    
    patrones = {
        "nombre": r"nombre[:\-]?\s*(.+)",
        "telefono": r"tel[eé]fono[:\-]?\s*(\d{7,10})",
        "direccion": r"direcci[oó]n[:\-]?\s*(.+)",
        "ciudad": r"ciudad[:\-]?\s*(.+)"
    }
    
    for campo, patron in patrones.items():
        match = re.search(patron, mensaje, re.IGNORECASE)
        if match:
            datos[campo] = match.group(1).strip()
    
    campos_faltantes = [campo for campo in patrones.keys() if campo not in datos]
    
    if campos_faltantes:
        return {"error": f"⚠️ Faltan datos: {', '.join(campos_faltantes)}. Por favor, envíalos en el formato adecuado."}
    
    return datos
