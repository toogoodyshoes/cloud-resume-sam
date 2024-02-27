import sys
import os
import moto
from unittest import TestCase
from boto3 import resource, client

sys.path.append('./')
from update_count.count import LambdaDynamoDBClass
from update_count.count import increment, check_item, create_item, update_item, return_count

@moto.mock_aws
class TestLambda(TestCase):
    def setUp(self) -> None:

        # Mock enviroment and overrrides
        self.test_ddb_table_name = "unit_test_ddb"
        os.environ["DYNAMODB_TABLE_NAME"] = self.test_ddb_table_name

        dynamodb = resource('dynamodb', region_name='ap-south-1')
        dynamodb.create_table(
            TableName=self.test_ddb_table_name,
            KeySchema=[
                {
                    'AttributeName': 'user',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        mocked_dynamodb_resource = resource("dynamodb", region_name='ap-south-1')
        mocked_dynamodb_resource = { 
            "resource" : resource('dynamodb', region_name='ap-south-1'),
            "table_name" : self.test_ddb_table_name
        }

        self.mocked_dynamodb_class = LambdaDynamoDBClass(mocked_dynamodb_resource)

    def test_hello(self):
        print('hello!!!')

    def tearDown(self) -> None:
        dynamodb_resource = client("dynamodb", region_name="ap-south-1")
        dynamodb_resource.delete_table(TableName = self.test_ddb_table_name )

    
