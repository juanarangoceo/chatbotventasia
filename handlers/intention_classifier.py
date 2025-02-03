def clasificar_intencion(mensaje):
    """Detecta la intención del cliente según su mensaje."""
    
    palabras_clave = {
        "comprar": ["comprar", "quiero", "ordenar", "pedir"],
        "cafe": ["café", "espresso", "capuchino", "americano"],
        "preparacion": ["preparar", "hacer café", "cómo se hace"],
        "molienda": ["molido", "granos", "moler"],
        "diferencia": ["diferencia", "vs", "comparación"]
    }

    for intencion, palabras in palabras_clave.items():
        if any(palabra in mensaje.lower() for palabra in palabras):
            return intencion

    return "desconocido"
