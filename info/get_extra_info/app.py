import json
from utils import (  # type: ignore
    Database, set_response_headers, convert_datetime_in_dict
)

HEADER = 'GET'


def create_response(status_code, message, results=None):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message, 'results': results}),
        'headers': set_response_headers(HEADER)
    }


def execute_query(connection, userId):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM portfolio WHERE userId = %s'
        cursor.execute(query, (userId,))
        return cursor.fetchone()


def lambda_handler(event, context):
    connection = None
    try:
        user_id = event['pathParameters']['userId']
        connection = Database.connect()
        results = execute_query(connection, user_id)
        if not results:
            return create_response(404, 'error', 'No results found.')
        final_results = [convert_datetime_in_dict(results)]
        return create_response(200, 'success', final_results)
    except Exception as e:
        print(str(e))
        return create_response(500, 'error', str(e))
    finally:
        print('end of try except block')
