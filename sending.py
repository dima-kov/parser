from handler import connection
from handler.consumer import MessageHandler

connection = connection.start_connection()

h = MessageHandler(connection, 3)
h.send('urls', 'hello my dear')
connection.close()
