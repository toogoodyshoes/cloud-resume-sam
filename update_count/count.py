import boto3

dynamodb = boto3.resource('dynamodb')

def increment(event, context):
    table = dynamodb.Table('vis-count')
    
    response = table.get_item(
        Key={'user': 'nihar'}
    )
    
    if 'Item' in response:
        response.clear()
        response = table.update_item(
            Key={'user': 'nihar'},
            UpdateExpression='SET v_count = v_count + :val',
            ExpressionAttributeValues={
                ':val': 1
            }
        )
    else:
        response.clear()
        response = table.put_item(
            Item={
                'user': 'nihar',
                'v_count': 1,
            }
        )
        
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        res = table.get_item(
            Key={'user': 'nihar'}
        )
        count = res['Item']['v_count']
        http_res = {
                "message": {
                    "visitor_count": count,
                }
            }
    else:
        http_res = {
                "message": "Update operation failed!"
            }
        

    return http_res