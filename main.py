import config
from pqueue.connection import start_connection
from pqueue.consumer import MessageConsumer
from pqueue.producer import MessageProducer
from parser import Parser
from storage import GoogleSheetsStorage


def populate_start_queue():
    for keyword in config.START_KEYWORDS:
        queue_producer.send("https://www.google.com.ua/search?q={}+articles".format(keyword))
    print("Sent urls with start keywords searches")


rabbitMQ = start_connection()

google_sheets = GoogleSheetsStorage()
queue_producer = MessageProducer(rabbitMQ)
parser = Parser(queue_producer, google_sheets)
message_consumer_thread = MessageConsumer(rabbitMQ, parser, config.QUEUE_NAME)

populate_start_queue()

try:
    message_consumer_thread.start()
except KeyboardInterrupt:
    message_consumer_thread.close()
    rabbitMQ.close()


