from os import environ
from boto3 import resource

_LAMBDA_DYNAMODB_RESOURCE = { 
    "resource" : resource('dynamodb', region_name='ap-south-1'), 
    "table_name" : environ.get("DYNAMODB_TABLE_NAME","NONE") 
}

class LambdaDynamoDBClass:
    def __init__(self, lambda_dynamodb_resource):
        self.resource = lambda_dynamodb_resource["resource"]
        self.table_name = lambda_dynamodb_resource["table_name"]
        self.table = self.resource.Table(self.table_name)

# Handler
def increment(event, context):

    global _LAMBDA_DYNAMODB_RESOURCE

    dynamodb_resource_class = LambdaDynamoDBClass(_LAMBDA_DYNAMODB_RESOURCE)
    
    response = check_item(dynamo_db=dynamodb_resource_class)
    
    if 'Item' in response:
        response.clear()
        response = update_item(dynamo_db=dynamodb_resource_class)
    else:
        response.clear()
        response = create_item(dynamo_db=dynamodb_resource_class)
        
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return send_count(dynamo_db=dynamodb_resource_class)
    else:
        return {
                "message": "Update operation failed!"
        }

# Helper Functions
def check_item(dynamo_db: LambdaDynamoDBClass):
    return dynamo_db.table.get_item(
        Key={'user': 'nihar'}
    )

def create_item(dynamo_db: LambdaDynamoDBClass):
    return dynamo_db.table.put_item(
        Item={
            'user': 'nihar',
            'v_count': 1,
        }
    )

def update_item(dynamo_db: LambdaDynamoDBClass):
    return dynamo_db.table.update_item(
        Key={'user': 'nihar'},
        UpdateExpression='SET v_count = v_count + :val',
        ExpressionAttributeValues={
                ':val': 1
        }
    )

def send_count(dynamo_db: LambdaDynamoDBClass):
    response = dynamo_db.table.get_item(
        Key={'user': 'nihar'}
    )

    count = response['Item']['v_count']

    return {
        "message": {
            "visitor_count": count,
        }
    }