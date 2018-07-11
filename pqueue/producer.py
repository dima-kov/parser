from pqueue import QUEUE_NAME as DEFAULT_QUEUE_NAME


class MessageProducer():
    connection = None

    def __init__(self, connection):
        self.channel = connection.channel()

    def send(self, body, queue_name=DEFAULT_QUEUE_NAME):
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=body
        )
