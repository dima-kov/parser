import asyncio
import threading

from pqueue import QUEUE_NAME as DEFAULT_QUEUE_NAME


class MessageConsumer(threading.Thread):

    parser = None

    def __init__(self, connection, parser, queue=DEFAULT_QUEUE_NAME):
        threading.Thread.__init__(self)
        self.channel = connection.channel()
        self.queue = queue
        self.channel.queue_declare(queue=self.queue)

        if parser is None:
            raise ValueError("Parser cannot be None")
        self.parser = parser
        print("Message Consumer init")

    def run(self):
        print("Message Consumer start")
        self.handle_input()

    def handle_input(self):
        self.channel.basic_consume(self.on_message, self.queue, no_ack=True)
        print("Message Consumer start consuming")
        self.channel.start_consuming()

    def on_message(self, channel, method_frame, header_frame, body):
        print("Message received: ", body)
        self.parser.parse(body.decode("utf-8"))

    def close(self):
        print("Gracefully exit")
        self.channel.stop_consuming()
