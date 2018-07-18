from storage_facade import StorageFacade


class QueueHandler(object):

    parser = None
    storage_facade = None

    def __init__(self, parser, storage_facade: StorageFacade):

        if parser is None:
            raise ValueError("Parser cannot be None")
        self.parser = parser
        self.storage_facade = storage_facade
        print("Queue Handler inited")

    async def run(self):
        await self.handle()

    async def handle(self):
        while not self.storage_facade.queue_empty():
            queue_item = self.storage_facade.get_url_from_queue()
            await self.handle_queue_message(queue_item)

    async def handle_queue_message(self, message):
        print("Message received: ", message)
        await self.parser.parse(message)
