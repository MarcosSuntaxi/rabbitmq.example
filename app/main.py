from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika

app = FastAPI()

# Modelo del body del POST
class TextoEntrada(BaseModel):
    mensaje: str

@app.post("/enviar")
def enviar_mensaje(data: TextoEntrada):
    try:
        # Conexión a RabbitMQ en localhost
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declarar la cola
        channel.queue_declare(queue='cola_texto')

        # Enviar mensaje
        channel.basic_publish(exchange='', routing_key='cola_texto', body=data.mensaje.encode())
        connection.close()

        return {"estado": "ok", "mensaje": data.mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
