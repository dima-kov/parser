from handler import QueueHandlerThread
from parser import Parser

from pqueue import ParsingQueue

queue = ParsingQueue()

parser = Parser(queue)
queue_handler_thread = QueueHandlerThread(parser, queue)

try:
    queue_handler_thread.start()
except KeyboardInterrupt:
    print("EXITS")
    queue.join()
