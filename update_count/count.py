from os import environ
from boto3 import resource
import hashlib

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

    source_ip = event['requestContext']['http']['sourceIp']
    hasher = hashlib.sha256()
    hasher.update(source_ip.encode('utf-8'))
    hashed_ip = hasher.hexdigest()

    response = check_item(dynamo_db=dynamodb_resource_class)

    if 'Item' in response:
        update_count(dynamo_db=dynamodb_resource_class, hashed_ip=hashed_ip)
    else:
        create_item(dynamo_db=dynamodb_resource_class, hashed_ip=hashed_ip)

    return send_count(dynamo_db=dynamodb_resource_class)

# Check if the item is present in DB
def check_item(dynamo_db: LambdaDynamoDBClass):
    return dynamo_db.table.get_item(
        Key={'user': 'nihar'}
    )

# Add item to DB
def create_item(dynamo_db: LambdaDynamoDBClass, hashed_ip: str):
    return dynamo_db.table.put_item(
        Item={
            'user': 'nihar',
            'v_count': 1,
            'visitors': [hashed_ip]
        }
    )

# Update the count in DB
def update_count(dynamo_db: LambdaDynamoDBClass, hashed_ip: str):
    response = dynamo_db.table.get_item(
        Key={'user': 'nihar'}
    )

    visitors = response['Item']['visitors']
    if hashed_ip in visitors:
        return
    visitors.append(hashed_ip)

    return dynamo_db.table.update_item(
        Key={'user': 'nihar'},
        UpdateExpression='SET v_count = v_count + :val, visitors = :new_vis',
        ExpressionAttributeValues={
                ':val': 1,
                ':new_vis': visitors
        }
    )

# Return the visitor count
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