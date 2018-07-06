from handler import connection
from handler.producer import MessageProducer

connection = connection.start_connection()

h = MessageProducer(connection)
h.send('urls', 'hello my dear')
connection.close()
