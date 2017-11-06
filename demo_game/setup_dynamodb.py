import boto3
from game import DYNAMODB_HISTORY_TABLE
def setup_environment():
    client = boto3.client('dynamodb')
    try:
        response = client.describe_table(
        TableName=DYNAMODB_HISTORY_TABLE
        )
        print("Table exists, close")
    except client.exceptions.ResourceNotFoundException:
        print("Create Table {}".format(DYNAMODB_HISTORY_TABLE))
        table = client.create_table(
            TableName=DYNAMODB_HISTORY_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'game_number',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'game_number',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

#check if table exists
setup_environment()
