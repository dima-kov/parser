import asyncio
import time

from mongoengine import connection

from config import MONGO_DB_NAME
from config import MONGO_HOST
from config import MONGO_PORT
from mongo import PageMongoStorage
from qhandler import QueueHandler
from parser import Parser
from pqueue import ParsingQueue
from storage_facade import StorageFacade

"""
                             |¯¯¯¯¯|       |¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                             |     | ===== |              |
        |¯¯¯¯¯¯¯¯¯¯¯¯¯¯|     |     |       |    Parser    |
        |    Queue     | ⇒⇒⇒ |  F  | ===== |              |
        |              |     |  A  |       |              |
        ¯¯¯¯¯¯¯⇑¯¯¯¯¯¯¯      |  C  |       ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
               ⇑             |  A  |
               ⇑             |  D  |
        |¯¯¯¯¯¯¯¯¯¯¯¯¯¯|     |  E  |       |¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
        |    Mongo     | ⇒⇒⇒ |     |       |    Queue     |
        |              |     |     | ===== |   Handler    |
        ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯      |     |       |              |
                             |_____|       ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

"""

loop = asyncio.get_event_loop()

connection.connect(MONGO_DB_NAME, host=MONGO_HOST, port=MONGO_PORT)

queue = ParsingQueue()
mongo = PageMongoStorage()
facade = StorageFacade(mongo, queue)

parser = Parser(facade, loop)

threads = 20
try:
    workers = [asyncio.ensure_future(QueueHandler(parser, facade).run()) for i in range(threads)]
    loop.run_until_complete(asyncio.wait(workers))
except KeyboardInterrupt:
    loop.close()
    print("START EXIT")
