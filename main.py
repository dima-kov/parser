import asyncio
import time

from mongoengine import connection

from config import MONGO_DB_NAME
from config import MONGO_HOST
from config import MONGO_PORT
from document import Page
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

start = time.time()
non_parsed_before = Page.objects.get_non_parsed().count()
parsed_before = Page.objects.get_parsed().count()
try:
    q_handler.run()
except KeyboardInterrupt:
    print("Gracefully exit")
    print("Time: ", time.time() - start)
    print("Non parsed after: ", Page.objects.get_non_parsed().count() - non_parsed_before)
    print("Parsed after: ", Page.objects.get_parsed().count() - parsed_before)
    q_handler.close()
    loop.close()
