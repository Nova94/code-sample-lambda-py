import boto3
import pytest
import json
import handler
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
    res = json.loads(handler.get({'pathParameters': None}, {}))
    assert len(res['body']) == len(values)
    assert res['statusCode'] == 200

    # get item
    for i, value in enumerate(values):
        key = environ['keyName'] + str(i)
        res = json.loads(handler.get({'pathParameters': {'id': key}}, {}))
        res['body']
        assert len(res['body']) == 2
        assert res['statusCode'] == 200

    # no existing item
    res = json.loads(handler.get({'pathParameters': {'id': 'NoneExisting'}}, {}))
    assert res['statusCode'] == 404


@mock_dynamodb2
def test_create():
    values = setup_table()
    res = json.loads(handler.create({'headers': {'Accept': 'application/json'}, 'body': json.dumps({'list': ['one', 'two']})}, {}))
    assert res['statusCode'] == 200
    assert res['body']['errors'] == []

    # check that it was added
    res = json.loads(handler.get({'pathParameters': None}, {}))
    assert len(res['body']) == len(values) + 1
    assert res['statusCode'] == 200

    # multiple key values added
    res = json.loads(handler.create({'headers': {'Accept': 'application/json'},
                                     'body': json.dumps({'list': ['one', 'two'], 'dict': {"hello": "world"}})}, {}))
    assert res['statusCode'] == 200
    assert res['body']['errors'] == []

    # check that overrides list and dict was added
    res = json.loads(handler.get({'pathParameters': None}, {}))
    assert len(res['body']) == len(values) + 2
    assert res['statusCode'] == 200

    # returns 415 without application/json header
    res = json.loads(handler.create({'body': json.dumps({'list': ['one', 'two']})}, {}))
    assert res['statusCode'] == 415

    # returns 400 with application/json header and bad json
    res = json.loads(handler.create({'headers': {'Accept': 'application/json'}, 'body': {'list': ['one', 'two']}}, {}))
    assert res['statusCode'] == 400

@mock_dynamodb2
def test_delete():
    values = setup_table()
    res = json.loads(
        handler.create({'headers': {'Accept': 'application/json'}, 'body': json.dumps({'list': ['one', 'two']})}, {}))
    assert res['statusCode'] == 200
    assert res['body']['errors'] == []

    # check that it was added
    res = json.loads(handler.get({'pathParameters': None}, {}))
    assert len(res['body']) == len(values) + 1
    assert res['statusCode'] == 200

    # delete key0
    res = json.loads(handler.delete({'pathParameters': {'id': 'Key0'}}, {}))
    assert res['statusCode'] == 200
    assert res['body'] == {'Key': 'Key0', 'Value': 'world'}

    # delete key0
    res = json.loads(handler.delete({'pathParameters': {'id': 'None'}}, {}))
    assert res['statusCode'] == 404
    assert res['body'] is None
