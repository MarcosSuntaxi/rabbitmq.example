import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='cola_texto')

def callback(ch, method, properties, body):
    print(f"[x] Recibido: {body.decode()}")

channel.basic_consume(queue='cola_texto', on_message_callback=callback, auto_ack=True)

print("[*] Esperando mensajes. Presiona CTRL+C para salir")
channel.start_consuming()
