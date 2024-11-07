import os
from dotenv import load_dotenv
import pymysql  # type: ignore
from datetime import datetime
import json

current_directory = os.path.dirname(__file__)
env_path = os.path.join(current_directory, '.env')
load_dotenv(dotenv_path=env_path)


class Database:
    @staticmethod
    def connect():
        """Create and return a new database connection."""
        return pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )

    @staticmethod
    def close(connection):
        """Close the provided database connection."""
        if connection:
            connection.close()


def set_response_headers(METHOD_TYPE):
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': f'OPTIONS,{METHOD_TYPE}',
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


def create_response(status_code, METHOD_TYPE, message, results=None):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message, 'results': results}),
        'headers': set_response_headers(METHOD_TYPE)
    }
