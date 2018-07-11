from storage.storage import Storage
from config import

import pymongo



class MongoStorage(Storage):

    def __init__(self, ):
        connection_str = 'mongodb://{}:{}'.format()
        self.client = pymongo.MongoClient()



    def insert(self, values):
        pass

    def get_by_id(self, id):
        pass
