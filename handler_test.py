import boto3
import pytest
import json
import handler
from os import environ
from moto import mock_dynamodb2

keyName = environ['keyName']


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
        test.put_item(Item={keyName: key, 'Value': value})
    return values


@mock_dynamodb2
def test_get():
    values = setup_table()
    # get all
    res = handler.get({'pathParameters': None}, {})
    print(res)
    assert len(json.loads(res['body'])) == len(values)
    assert res['statusCode'] == 200

    # get item
    for i, value in enumerate(values):
        key = environ['keyName'] + str(i)
        res = handler.get({'pathParameters': {'id': key}}, {})
        print(res)
        assert len(json.loads(res['body'])) == 2
        assert res['statusCode'] == 200

    # no existing item
    res = handler.get({'pathParameters': {'id': 'NoneExisting'}}, {})
    print(res)
    assert res['statusCode'] == 404


@mock_dynamodb2
def test_create():
    values = setup_table()
    res = handler.create({'headers': {'Accept': 'application/json'}, 'body': json.dumps({'list': ['one', 'two']})}, {})
    print(res)
    assert res['statusCode'] == 200
    assert json.loads(res['body'])['errors'] == []

    # check that it was added
    res = handler.get({'pathParameters': None}, {})
    print(res)
    assert len(json.loads(res['body'])) == len(values) + 1
    assert res['statusCode'] == 200

    # multiple key values added
    res = handler.create({'headers': {'Accept': 'application/json'},
                          'body': json.dumps({'list': ['one', 'two'], 'dict': {"hello": 1.0}})}, {})
    print(res)
    assert res['statusCode'] == 200
    assert json.loads(res['body'])['errors'] == []

    # check that overrides list and dict was added
    res = handler.get({'pathParameters': None}, {})
    print(res)
    assert len(json.loads(res['body'])) == len(values) + 2
    assert res['statusCode'] == 200

    # returns 415 without application/json header
    res = handler.create({'body': json.dumps({'list': ['one', 'two']})}, {})
    print(res)
    assert res['statusCode'] == 415

    # returns 400 with application/json header and bad json
    res = handler.create({'headers': {'Accept': 'application/json'}, 'body': {'list': ['one', 'two']}}, {})
    print(res)
    assert res['statusCode'] == 400


@mock_dynamodb2
def test_update():
    values = setup_table()

    # update single and check response
    res = handler.update({'pathParameters': {'id': 'Key0'}, 'queryStringParameters': {'value': 'updated'}}, {})
    print(res)
    assert res['statusCode'] == 200

    # multiple key values updated and check response
    res = handler.update({'pathParameters': None, 'queryStringParameters': None,
                          'headers': {'Accept': 'application/json'},
                          'body': json.dumps({'Key1': ['one', 'two'], 'Key2': {"hello": "world"}})}, {})
    print(res)
    assert res['statusCode'] == 200

    # check that they were updated
    res = handler.get({'pathParameters': {'id': 'Key0'}}, {})
    print(res)
    assert json.loads(res['body']) == {keyName: 'Key0', 'Value': 'updated'}
    assert res['statusCode'] == 200

    # returns 415 without application/json header
    res = handler.update({'pathParameters': None, 'queryStringParameters': None,
                          'body': json.dumps({'list': ['one', 'two']})}, {})
    print(res)
    assert res['statusCode'] == 415

    # returns 400 with application/json header and bad json
    res = handler.update({'pathParameters': None, 'queryStringParameters': None,
                          'headers': {'Accept': 'application/json'}, 'body': {'list': ['one', 'two']}}, {})
    print(res)
    assert res['statusCode'] == 400


@mock_dynamodb2
def test_delete():
    values = setup_table()
    res = handler.create({'headers': {'Accept': 'application/json'}, 'body': json.dumps({'list': ['one', 'two']})}, {})
    print(res)
    assert res['statusCode'] == 200
    assert json.loads(res['body'])['errors'] == []

    # check that it was added
    res = handler.get({'pathParameters': None}, {})
    print(res)
    assert len(json.loads(res['body'])) == len(values) + 1
    assert res['statusCode'] == 200

    # delete key0
    res = handler.delete({'pathParameters': {'id': 'Key0'}}, {})
    print(res)
    assert res['statusCode'] == 200
    assert json.loads(res['body']) == {keyName: 'Key0', 'Value': 'world'}

    # delete None
    res = handler.delete({'pathParameters': {'id': 'None'}}, {})
    print(res)
    assert res['statusCode'] == 404
    assert json.loads(res['body']) == {}
