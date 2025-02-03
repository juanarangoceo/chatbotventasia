import openai
import json

with open("config.json", "r") as f:
    config = json.load(f)

openai.api_key = config["OPENAI_API_KEY"]

def clasificar_intencion(mensaje):
    prompt = f"""
    Actúa como un experto en ventas de cafeteras. Responde de manera breve y persuasiva, resaltando características clave del producto.

    Cliente: {mensaje}
    """

    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=100
    )

    return respuesta["choices"][0]["message"]["content"].strip()
