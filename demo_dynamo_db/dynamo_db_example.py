import boto3
from boto3.dynamodb.conditions import Key, Attr


def setup_table(conn):
    table = conn.create_table(
        TableName='game_history',
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
    table.meta.client.get_waiter('table_exists').wait(TableName='game_history')


def ex1_write_record(conn):
    table = dynamodb.Table('game_history')
    table.put_item(
        Item={
            'user_id': '1',
            'game_number': 1,
            'game_moves': "{}",
            'game_score': '1'
        }
    )
    response = table.get_item(
        Key={
            'user_id': '1',
            'game_number': 1
        }
    )
    print("item {}".format(response["Item"]))


def ex2_write_record(conn):
    table = dynamodb.Table('game_history')
    table.put_item(
        Item={
            'user_id': '1',
            'game_number': 2,
            'game_moves': "{}",
            'game_score': '2'
        }
    )
    response = table.get_item(
        Key={
            'user_id': '1',
            'game_number': 2
        }
    )
    print("1. item {}".format(response["Item"]))

    table.put_item(
        Item={
            'user_id': '1',
            'game_number': 2,
            'game_moves': "{}",
            'game_score': 'new score'
        }
    )
    response = table.get_item(
        Key={
            'user_id': '1',
            'game_number': 2
        }
    )
    # new record will overwrite old
    print("2. item: {}".format(response["Item"]))


def ex3_write_record(conn):
    # write new score record to user (primary id)
    table = dynamodb.Table('game_history')
    table.put_item(
        Item={
            'user_id': '1',
            'game_number': 1,
            'game_moves': "{}",
            'game_score': '2'
        }
    )
    table.put_item(
        Item={
            'user_id': '1',
            'game_number': 2,
            'game_moves': "{}",
            'game_score': 'new score'
        }
    )
    # get user all games
    response = table.query(
        KeyConditionExpression=Key('user_id').eq('1')
    )
    print("Items: {}".format(response['Items']) )


def ex4_write_batch_records(conn):
    table = dynamodb.Table('game_history')

    with table.batch_writer() as batch:
        for i in range(50):
            batch.put_item(
                Item={
                    'user_id': '1',
                    'game_number': i,
                    'game_moves': "{}",
                    'game_score': 'new score {}'.format(i)
                }
            )
    response = table.query(
        KeyConditionExpression=Key('user_id').eq('1')
    )
    print("Items: {}".format(["Game: {game_number} Score: {game_score} \n".format(**i) for i in response['Items']]) )



# Get the service resource.
dynamodb = boto3.resource('dynamodb')

print("I. Setup table...")
setup_table(dynamodb)
#write single record
print("II. Write single record to table.")
ex1_write_record(dynamodb)

#update/overwrite the record
print("III. Write single record to table.")
ex2_write_record(dynamodb)

#add record to primary key
print("III. Add new record to primary key.")
ex3_write_record(dynamodb)

#batch insert to dynamo db
print("IV. Insert many records ")
ex4_write_batch_records(dynamodb)

# drop table
print("V. Drop table")
dynamodb.Table('game_history').delete()