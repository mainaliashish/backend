def lambda_handler(event, context):
    try:
        print('Hello World')
    except Exception as e:
        print(e)
    finally:
        print('end of try except block')
