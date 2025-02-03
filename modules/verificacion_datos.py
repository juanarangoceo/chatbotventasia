def validar_datos_cliente(mensaje, cliente_id, usuarios):
    """Verifica y almacena los datos del cliente."""
    datos = usuarios[cliente_id].get("datos", {})

    partes = mensaje.split("\n")
    if len(partes) >= 1: datos["nombre"] = partes[0]
    if len(partes) >= 2: datos["telefono"] = partes[1]
    if len(partes) >= 3: datos["direccion"] = partes[2]
    if len(partes) >= 4: datos["ciudad"] = partes[3]

    faltantes = []
    if "nombre" not in datos: faltantes.append("1️⃣ *Nombre* 😊")
    if "telefono" not in datos: faltantes.append("2️⃣ *Teléfono* 📞")
    if "direccion" not in datos: faltantes.append("3️⃣ *Dirección* 🏡")
    if "ciudad" not in datos: faltantes.append("4️⃣ *Ciudad* 🏙")

    usuarios[cliente_id]["datos"] = datos
    return faltantes
