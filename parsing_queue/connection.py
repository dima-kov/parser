
import pika

from config.settings import URL, USER, PASSWORD, VIRTUAL_HOST


def start_connection():
    credentials = pika.PlainCredentials(
        USER, PASSWORD
    )

    connection_params = pika.ConnectionParameters(URL, credentials=credentials, virtual_host=VIRTUAL_HOST)

    return pika.BlockingConnection(connection_params)
