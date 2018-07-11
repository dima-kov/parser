from pqueue import connection
from pqueue.producer import MessageProducer

connection = connection.start_connection()

h = MessageProducer(connection)
h.send('urls', 'darling')
connection.close()
