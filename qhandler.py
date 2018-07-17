import threading

from storage_facade import StorageFacade


class QueueHandlerThread(threading.Thread):

    parser = None
    storage_facade = None

    def __init__(self, parser, storage_facade: StorageFacade):
        threading.Thread.__init__(self)

        if parser is None:
            raise ValueError("Parser cannot be None")
        self.parser = parser
        self.storage_facade = storage_facade
        print("Queue Handler inited")

    def run(self):
        print("Queue Handler started")
        self.handle()

    def handle(self):
        while True:
            queue_item = self.storage_facade.get_url_from_queue()
            self.handle_queue_message(queue_item)

    def handle_queue_message(self, message):
        print("Message received: ", message)
        self.parser.parse(message)
