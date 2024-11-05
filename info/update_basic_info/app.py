import json
from utils import (  # type: ignore
    Database, set_response_headers, convert_datetime_in_dict
)

HEADER = 'PUT'


def create_response(status_code, message, results=None):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message, 'results': results}),
        'headers': set_response_headers(HEADER)
    }


def fetch_existing_user(cursor, userId):
    query = '''SELECT name, email, phoneNumber FROM users WHERE id = %s'''
    cursor.execute(query, userId)
    row = cursor.fetchone()
    return convert_datetime_in_dict(row) if row else None


def update_faq(cursor, user_data, userId):
    update_query = '''
    UPDATE faqs
    SET
        name = %s,
        email = %s,
        phoneNumber = %s
    WHERE id = %s
    '''
    cursor.execute(update_query, (
        user_data['name'],
        user_data['email'], user_data['phoneNumber'],
        userId
    ))


def lambda_handler(event, context):
    connection = None
    try:
        userId = event['pathParameters']['id']
        body = json.loads(event['body'])
        connection = Database.connect()
        with connection.cursor() as cursor:
            existing_user = fetch_existing_user(cursor, userId)
            if not existing_user:
                return create_response(404, 'error', 'No results found')
            user_data = {
                'name': body.get('name', existing_user['name']),
                'email': body.get(
                    'email', existing_user['email']),
                'phoneNumber': body.get(
                    'phoneNumber', existing_user['phoneNumber']),
            }
            update_faq(cursor, user_data, userId)
            connection.commit()
        return create_response(200, 'success', user_data)
    except Exception as e:
        print(str(e))
        return create_response(500, 'error', str(e))
    finally:
        if connection:
            Database.close()
