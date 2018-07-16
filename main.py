from handler import QueueHandlerThread
from parser import Parser

from pqueue import prepopulate_queue

queue = prepopulate_queue()

parser = Parser(queue)
queue_handler_thread = QueueHandlerThread(parser, queue)

try:
    queue_handler_thread.start()
except KeyboardInterrupt:
    queue.join()
