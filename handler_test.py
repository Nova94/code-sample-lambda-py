import boto3
import pytest
import json
from handler import get, DynamoDBEncoder
from os import environ
from moto import mock_dynamodb2


def setup_table():
    client = boto3.client('dynamodb')
    response = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'Key',
                'AttributeType': 'S'
            },
        ],
        TableName=environ['tableName'],
        KeySchema=[
            {
                'AttributeName': 'Key',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    assert response['TableDescription']['TableName'] == 'test'

    dynamo = boto3.resource('dynamodb')
    test = dynamo.Table(environ['tableName'])

    values = ['world', 123, b'hello', True, None, ['hello', 'world'], {'hello', 'world'}, {'Hello': 'World'}]
    for i, value in enumerate(values):
        key = environ['keyName'] + str(i)
        print('adding item w/ key {} value {}'.format(key, value))
        test.put_item(Item={'Key': key, 'Value': value})
    return values


@mock_dynamodb2
def test_get():
    values = setup_table()
    # get all
    res = get({'pathParameters': None}, {})
    assert len(json.loads(res['body'])) == len(values)
    assert res['statusCode'] == 200

    # get item
    for i, value in enumerate(values):
        key = environ['keyName'] + str(i)
        res = get({'pathParameters': {'id': key}}, {})
        body = json.loads(res['body'])
        assert len(body) == 2
        assert res['statusCode'] == 200

    # no existing item
    res = get({'pathParameters': {'id': 'NoneExisting'}}, {})
    assert res['statusCode'] == 404



@mock_dynamodb2
def test_add():
    pass


@mock_dynamodb2
def test_update():
    pass

@mock_dynamodb2
def test_delete():
    pass
