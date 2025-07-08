from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
import json

app = FastAPI()

# Modelo del body del POST
class MensajeEntrada(BaseModel):
    direccion: str
    interseccion: str
    numero_casa: str
    latitud: str
    longitud: str
    tipo_lugar: str
    sector_punto_referencia: str
    fecha_hecho: str
    hora_aproximada_hecho: str
    enlace_fuente: str
    transcripción_de_video: str
    transcripción_de_audio: str

@app.post("/enviar")
def enviar_mensaje(data: MensajeEntrada):
    try:
        # Conexión a RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declarar la cola
        channel.queue_declare(queue='cola_texto')

        # Convertir el objeto a JSON string
        mensaje_json = json.dumps(data.dict(), ensure_ascii=False)

        # Publicar el mensaje
        channel.basic_publish(
            exchange='',
            routing_key='cola_texto',
            body=mensaje_json.encode('utf-8')
        )

        connection.close()
        return {"estado": "ok", "mensaje_enviado": data.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
