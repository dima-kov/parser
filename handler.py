import threading


class QueueHandlerThread(threading.Thread):

    parser = None

    def __init__(self, parser, queue):
        threading.Thread.__init__(self)
        if parser is None:
            raise ValueError("Parser cannot be None")
        self.parser = parser
        self.queue = queue
        print("Queue Handler inited")

    def run(self):
        print("Queue Handler started")
        self.handle()

    def handle(self):
        while True:
            queue_item = self.queue.get()
            self.handle_queue_message(queue_item)
            self.queue.task_done()

    def handle_queue_message(self, message):
        print("Message received: ", message)
        self.parser.parse(message)
