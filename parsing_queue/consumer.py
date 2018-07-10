from parsing_queue import QUEUE_NAME as DEFAULT_QUEUE_NAME


class MessageConsumer(object):

    parser = None

    def __init__(self, connection, parser, event_loop):
        self.channel = connection.channel()
        self.event_loop = event_loop
        if parser is None:
            raise ValueError("Parser cannot be None")
        self.parser = parser

    def handle_input(self, queue_name=DEFAULT_QUEUE_NAME):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_consume(self.on_message, queue_name, no_ack=True)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        return

    def on_message(self, channel, method_frame, header_frame, body):
        print("Message received: ", body)
        task = self.event_loop.create_task(self.parser.parse(body.decode("utf-8")))
        self.event_loop.run_until_complete(task)
