
import pika

USER, PASSWORD = 'bhkakfli', 'LP4wTuHX0d9FHtQ-IPNTlfm2wRzt2lhe'
URL = 'wolverine.rmq.cloudamqp.com'

VIRTUAL_HOST = 'bhkakfli'


def start_connection():
    credentials = pika.PlainCredentials(
        USER, PASSWORD
    )

    connection_params = pika.ConnectionParameters(URL, credentials=credentials, virtual_host=VIRTUAL_HOST)

    return pika.BlockingConnection(connection_params)
