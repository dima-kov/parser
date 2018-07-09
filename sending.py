from parsing_queue import connection
from parsing_queue.producer import MessageProducer

connection = connection.start_connection()

h = MessageProducer(connection)
h.send('urls', 'darling')
connection.close()
