import os
from dotenv import load_dotenv
from pymysql import pymysql  # type: ignore


current_directory = os.path.dirname(__file__)
env_path = os.path.join(current_directory, '.env')
load_dotenv(dotenv_path=env_path)


class Database:
    connection = None

    @classmethod
    def connect(cls):
        '''Establish connection with the database'''
        if cls.connection is None:
            cls.connection = pymysql.connect(
                host=os.environ.get('DB_HOST'),
                user=os.environ.get('DB_USERNAME'),
                password=os.environ.get('DB_PASSWORD'),
                database=os.environ.get('DB_NAME'),
                cursorclass=pymysql.cursors.DictCursor
            )
        return cls.connection

    @classmethod
    def close(cls):
        '''Close the database connection'''
        if cls.connection:
            cls.connection.close()
            cls.connection = None
