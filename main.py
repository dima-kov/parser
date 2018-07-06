from handler.connection import *
from handler.consumer import *

connection = start_connection()
h = MessageHandler(connection, 3)
h.subscribe('urls')
connection.close()
