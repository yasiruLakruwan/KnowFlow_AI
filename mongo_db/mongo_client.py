from pymongo import MongoClient

class MongoClientProvider:

    def __init__(self,uri:str,db_name:str):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]

    # Getting the db
    def get_db(self):
        return self._db
    
    # Closing the db
    def close(self):
        self._client.close()
    