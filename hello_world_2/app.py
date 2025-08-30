import json
from service.MockerService import MockService 

def lambda_handler(event, context):
    result = MockService().do_something()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world 2",
            "sharedService": result
        }),
    }
