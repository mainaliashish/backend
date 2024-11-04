import os
from dotenv import load_dotenv
import pymysql  # type: ignore
from datetime import datetime


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


def set_response_headers(header):
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': f'OPTIONS,{header}',
        'Access-Control-Allow-Headers': (
            'Content-Type,X-Amz-Date,Authorization,'
            'X-Api-Key,X-Amz-Security-Token'
        )
    }


def convert_datetime_in_dict(row):
    """Convert any datetime objects in a dictionary to strings."""
    converted_row = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            converted_row[key] = value.isoformat()
        else:
            converted_row[key] = value
    return converted_row
