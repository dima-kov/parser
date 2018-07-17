from mongoengine import connection

from config import MONGO_DB_NAME
from config import MONGO_HOST
from config import MONGO_PORT
from mongo import PageMongoStorage
from qhandler import QueueHandlerThread
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

connection.connect(MONGO_DB_NAME, host=MONGO_HOST, port=MONGO_PORT)

queue = ParsingQueue()
mongo = PageMongoStorage()
facade = StorageFacade(mongo, queue)

parser = Parser(facade)
queue_handler_thread = QueueHandlerThread(parser, facade)

try:
    queue_handler_thread.start()
except KeyboardInterrupt:
    print("EXITS")
    queue.join()
