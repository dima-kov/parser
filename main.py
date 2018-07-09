import asyncio
from config import QUEUE_NAME
from parsing_queue.connection import start_connection
from parsing_queue.consumer import MessageConsumer
from parsing_queue.producer import MessageProducer
from parser.parse import Parser


rabbitMQ_conn = start_connection()

queue_producer = MessageProducer(rabbitMQ_conn)
parser = Parser(queue_producer)
queue_consumer = MessageConsumer(rabbitMQ_conn, parser)

START_KEYWORDS = ['IT', 'programming', 'AI', 'machine learning', 'technologies', 'startup', 'investing', 'blockchain']

for keyword in START_KEYWORDS:
    queue_producer.send("https://www.google.com.ua/search?q={}+articles".format(keyword))
print("Sent urls with start keywords searches")

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(queue_consumer.handle_input(QUEUE_NAME)))
loop.close()
