import asyncio

from storage_facade import StorageFacade


class QueueHandler(object):

    parser = None
    storage_facade = None
    threads = 10

    def __init__(self, loop, parser, storage_facade: StorageFacade):
        self.loop = loop
        self.parser = parser
        self.parser.set_loop(loop)
        self.storage_facade = storage_facade
        print("Queue Handler inited")

    def run(self):
        workers = []
        for _ in range(self.threads):
            workers.append(asyncio.ensure_future(self.handle()))
        self.loop.run_until_complete(asyncio.wait(workers))

    async def handle(self):
        while not self.storage_facade.queue_empty():
            queue_item = self.storage_facade.get_url_from_queue()
            try:
                await self.handle_queue_message(queue_item)
            except:
                print("Error during processing: ", queue_item)

    async def handle_queue_message(self, message):
        print("Message received: ", message)
        await self.parser.parse(message)

    def close(self):
        pass
