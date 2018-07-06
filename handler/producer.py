class MessageProducer(object):
    connection = None

    def __init__(self, connection):
        self.channel = connection.channel()

    def send(self, queue_name, body):
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=body
        )
