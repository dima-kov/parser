import asyncio

from config import QUEUE_NAME
from pqueue.connection import start_connection
from pqueue.consumer import MessageConsumer
from pqueue.producer import MessageProducer
from parser import Parser


rabbitMQ = start_connection()

queue_producer = MessageProducer(rabbitMQ)
parser = Parser(queue_producer)
message_consumer_thread = MessageConsumer(rabbitMQ, parser, QUEUE_NAME)

START_KEYWORDS = ['IT', 'programming', 'AI', 'machine+learning', 'technologies', 'startup', 'investing', 'blockchain']

for keyword in START_KEYWORDS:
    queue_producer.send("https://www.google.com.ua/search?q={}+articles".format(keyword))

print("Sent urls with start keywords searches")

try:
    message_consumer_thread.start()
except KeyboardInterrupt:
    message_consumer_thread.close()
    rabbitMQ.close()
