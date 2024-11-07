import json
from utils import (  # type: ignore
    Database, create_response
)

METHOD_TYPE = 'POST'


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
        return create_response(201, METHOD_TYPE, 'success', contact_data)

    except Exception as e:
        print(str(e))
        return create_response(500, METHOD_TYPE, 'error', str(e))
    finally:
        Database.close(connection)
