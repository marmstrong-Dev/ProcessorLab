"""
File needed to set up a connection to MongoDB
Using PyMongo for db connection
Class will need methods to:
    - connect to db
    - disconnect from db

Will use .env file to store connection uri (loaded in app.py)

Will use singleton pattern to ensure only one connection is made
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os


class DataCon:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DataCon.__instance is None:
            DataCon()
        return DataCon.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DataCon.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            load_dotenv()
            self.client = MongoClient(os.getenv("MONGO_URI"))
            self.db = self.client[os.getenv("DB_NAME")]
            DataCon.__instance = self

    def get_db(self):
        return self.db

    def close(self):
        self.client.close()
