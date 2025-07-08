# rabbitmq.example

Este repositorio es un ejemplo sencillo de integración entre una API REST construida con FastAPI y un sistema de colas de mensajes usando RabbitMQ.

## Descripción

El proyecto contiene dos componentes principales:

1. **API REST (FastAPI)**: expone un endpoint `/enviar` donde se puede enviar un mensaje (texto) mediante una petición POST. El mensaje recibido se publica en una cola llamada `cola_texto` en RabbitMQ.

2. **Consumidor de RabbitMQ**: un script que escucha la cola `cola_texto` y muestra en consola los mensajes recibidos.

## Estructura del repositorio

```
.
├── app/
│   ├── main.py
│   └── requirements.txt
└── consumidor.py
```

- `app/main.py`: Código de la API REST que recibe mensajes y los envía a RabbitMQ.
- `app/requirements.txt`: Dependencias necesarias para ejecutar la API.
- `consumidor.py`: Script que consume y muestra los mensajes de la cola.

## Requisitos

- Python 3.8 o superior
- RabbitMQ instalado y corriendo en `localhost`
- Dependencias de Python (ver instrucciones abajo)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/MarcosSuntaxi/rabbitmq.example.git
   cd rabbitmq.example
   ```

2. **Instalar dependencias de la API**
   ```bash
   cd app
   pip install -r requirements.txt
   cd ..
   ```

3. **Instalar dependencias para el consumidor**
   ```bash
   pip install pika
   ```

## Ejecución

### 1. Levantar el servidor de RabbitMQ

Asegúrate de tener RabbitMQ corriendo en tu máquina local. Si tienes Docker, puedes ejecutarlo con:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 2. Ejecutar la API REST

Desde la carpeta raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

### 3. Enviar mensajes a la API

Puedes enviar un mensaje usando `curl` o herramientas como Postman:

```bash
curl -X POST "http://127.0.0.1:8000/enviar" -H "Content-Type: application/json" -d '{"mensaje": "Hola mundo"}'
```

### 4. Ejecutar el consumidor

En otra terminal:

```bash
python consumidor.py
```

Este script recibirá y mostrará los mensajes enviados a la cola.

## Notas

- Puedes modificar el nombre de la cola cambiando el valor de `queue='cola_texto'` tanto en `main.py` como en `consumidor.py`.
- El ejemplo asume que RabbitMQ está en la misma máquina (`localhost`). Si usas otro host, actualiza los parámetros de conexión en ambos archivos.

## Licencia

MIT
