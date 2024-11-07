from utils import (  # type: ignore
    create_response,
    Database, convert_datetime_in_dict
)

METHOD_TYPE = 'GET'


def execute_query(connection, userId):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM users WHERE userId = %s'
        cursor.execute(query, (userId,))
        return cursor.fetchone()


def lambda_handler(event, context):
    connection = None
    userId = event['pathParameters']['userId']
    try:
        connection = Database.connect()
        results = execute_query(connection, userId)
        if not results:
            return create_response(404,
                                   METHOD_TYPE, 'error', 'No results found.')
        final_results = [convert_datetime_in_dict(results)]
        return create_response(200, METHOD_TYPE, 'success', final_results)
    except Exception as e:
        print(str(e))
        return create_response(500, METHOD_TYPE, 'error', str(e))
    finally:
        Database.close(connection)
