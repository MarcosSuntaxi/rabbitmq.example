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
- `app/requirements.txt`: Dependencias necesarias para ejecutar la API y el consumidor.
- `consumidor.py`: Script que consume y muestra los mensajes de la cola.

## Requisitos

- Python 3.8 o superior
- RabbitMQ instalado y corriendo en `localhost`
- Dependencias de Python (ver instrucciones abajo)

## Configuración de la cola en RabbitMQ

Por defecto, el código crea una cola llamada `cola_texto` de tipo **transient** (`durable=False`).  
Sin embargo, la mayoría de las instalaciones de RabbitMQ usan colas **durables** (`durable=True`) por defecto.  
Si intentas declarar una cola con el mismo nombre pero diferente configuración de durabilidad, RabbitMQ mostrará un error.

**Solución:**

- Puedes cambiar la configuración de la cola en ambos archivos (`app/main.py` y `consumidor.py`) para que sean coherentes.
- Si deseas que la cola sea durable (persistente), cambia la línea donde se declara la cola a:

```python
channel.queue_declare(queue='cola_texto', durable=True)
```

Asegúrate de usar la misma configuración en ambos archivos.

> **Nota:** Si ya creaste la cola con una configuración y la quieres cambiar, primero elimina la cola desde la interfaz de RabbitMQ o usa otro nombre de cola.

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/MarcosSuntaxi/rabbitmq.example.git
   cd rabbitmq.example
   ```

2. **Crear y activar un entorno virtual**  
   Es recomendable usar un entorno virtual para aislar las dependencias:
   ```bash
   # En sistemas Unix/macOS
   python3 -m venv venv
   source venv/bin/activate

   # En Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   Todas las dependencias necesarias (incluyendo `pika`) están en `app/requirements.txt`:
   ```bash
   pip install -r app/requirements.txt
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

En otra terminal (con el entorno virtual activado):

```bash
python consumidor.py
```

Este script recibirá y mostrará los mensajes enviados a la cola.

