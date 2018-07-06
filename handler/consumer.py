
class MessageHandler(object):
    connection = None
    parser = None

    def __init__(self, connection, parser):
        self.channel = connection.channel()
        if parser is None:
            raise ValueError("Parser cannot be None")
        self.parser = parser

    def subscribe(self, queue_name):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(self.on_message, queue_name)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        print(channel, method_frame, header_frame, body)

    def send(self, queue_name, body):
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=body
        )
