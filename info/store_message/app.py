import json
from utils import (  # type: ignore
    Database, set_response_headers
)

HEADER = 'POST'


def create_response(status_code, message, results=None):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message, 'results': results}),
        'headers': set_response_headers(HEADER)
    }


def create_note(cursor, contact_data):
    insert_query = '''
    INSERT INTO contact
    (userId, name, mobile, email, message)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        contact_data['userId'],
        contact_data['name'],
        contact_data['mobile'],
        contact_data['email'],
        contact_data['message'],
    ))


def lambda_handler(event, context):
    connection = None
    try:
        body = json.loads(event['body'])
        contact_data = {
            'userId': body['userId'],
            'name': body['name'],
            'mobile': body['mobile'],
            'email': body['email'],
            'message': body['message'],
        }
        connection = Database.connect()
        with connection.cursor() as cursor:
            create_note(cursor, contact_data)
            connection.commit()
        return create_response(201, 'success', contact_data)

    except Exception as e:
        print(str(e))
        return create_response(500, 'error', str(e))
    finally:
        if connection:
            Database.close()
