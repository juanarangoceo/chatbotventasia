def clasificar_intencion(mensaje):
    """
    Clasifica la intención del usuario.
    """
    mensaje = mensaje.lower().strip()
    
    if any(palabra in mensaje for palabra in ["hola", "buenos días", "buenas tardes", "buenas noches"]):
        return "saludo"
    
    if any(palabra in mensaje for palabra in ["precio", "cuánto cuesta", "valor"]):
        return "preguntar_precio"

    return "desconocido"
