import time

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

start = time.time()
threads_num = 4
try:
    for i in range(threads_num):
        queue_handler_thread = QueueHandlerThread(parser, facade)
        queue_handler_thread.start()
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print("EXITS")
    print("Threads: ", threads_num)
    print("Time: ", time.time() - start)
    queue.join()
