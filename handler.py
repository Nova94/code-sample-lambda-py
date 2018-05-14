import boto3
import logging
import json
import decimal
from os import environ
from botocore.exceptions import ClientError
from boto3.dynamodb.types import Binary

# logging init
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# environment variables
tableName = environ['tableName']
keyName = environ['keyName']
ttlName = environ['ttlName']

# dynamo table
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(tableName)


def get(event, context):
    """
    get key-value or all key-values from dynamodb
    :param event:
    :param context:
    :return: LambdaProxyResponse
    """
    try:
        params = event['pathParameters']
        if params is not None and 'id' in params:
            item = table.get_item(
                Key={
                    keyName: params['id']
                },
            )
            logger.info('{}'.format(item))

            if 'Item' in item:
                return {
                    'statusCode': 200,
                    'body': json.dumps(item['Item'], cls=DynamoDBEncoder)
                }
            else:
                return {'statusCode': 404}

        # TODO: handle when >1MB returned.
        items = table.scan()
        logger.info('{}'.format(items['Items']))
        return {
            'statusCode': 200,
            'body': json.dumps(items['Items'], cls=DynamoDBEncoder)
        }
    except ClientError as e:
        error = json.dumps(e.response['Error'])
        logger.error(error)
        return {'statusCode': 500, 'body': error}


def add(event, context):
    pass


def update(event, context):
    pass


def delete(event, context):
    pass


# Helper class to convert a DynamoDB item to JSON.
class DynamoDBEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, Binary):
            return o.__str__().decode('utf-8')
        elif isinstance(o, set):
            return list(o)
        return super(DynamoDBEncoder, self).default(o)
