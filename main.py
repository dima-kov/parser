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

parser = Parser(facade)
q_handler = QueueHandler(loop, parser, facade)

try:
    q_handler.run()
except KeyboardInterrupt:
    print("Gracefully exit")
    q_handler.close()
    loop.close()
