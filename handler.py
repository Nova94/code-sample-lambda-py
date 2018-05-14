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
            logger.info(item)

            if 'Item' in item:
                return Response(200, item['Item']).marshal()
            else:
                return Response(404).marshal()

        # TODO: handle when >1MB returned.
        items = table.scan()
        logger.info(items['Items'])
        return Response(200, items['Items']).marshal()
    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(500, error).marshal()


def create(event, context):
    """
    create function is used for creating new and overriding old key-value items
    :param event:
    :param context:
    :return: LambdaProxyResponse
    """
    errors = []
    try:
        if 'headers' in event and 'Accept' in event['headers'] and event['headers']['Accept'] == 'application/json':
            return put_items_from_body(errors, event)
        else:
            return Response(415).marshal()

    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(500, error).marshal()
    except TypeError as e:
        logger.error(e)
        return Response(400, 'Bad Request').marshal()


def update(event, context):
    errors = []
    try:
        pParams = event["pathParameters"]
        qParams = event["queryStringParameters"]
        if pParams is not None and qParams is not None and 'id' in pParams and 'value' in qParams:
            res = table.put_item(Item={keyName: pParams['id'], 'Value': qParams['value']},
                                 ConditionExpression="contains(Id, {})".format(pParams))
            logger.info(res)
            return Response(200).marshal()
        elif 'headers' in event and 'Accept' in event['headers'] and event['headers']['Accept'] == 'application/json':
            return put_items_from_body(errors, event)
        else:
            unaccept_content_type = Response(415, {"errors": "please use path/query param combo or application/json"}).marshal()
            logger.error(unaccept_content_type)
            return unaccept_content_type

    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(500, error).marshal()
    except TypeError as e:
        logger.error(e)
        return Response(400, 'Bad Request').marshal()


def put_items_from_body(errors, event):
    """
    puts k-v items from body into dynamodb
    :param errors:
    :param event:
    :param log:
    :return: LambdaProxyResponse
    """
    if event['body'] is not None:
        body = json.loads(event['body'])
        with table.batch_writer() as batch:
            try:
                for k, v in body.items():
                    res = batch.put_item(Item={keyName: k, 'Value': v})
                    logger.info(res)
            except ClientError as e:
                error = json.dumps(e.response['Error'])
                logger.error(error)
                errors.append(error)

        return Response(200, {'errors': errors}).marshal()
    else:
        return Response(400, {'errors': 'Bad Request'}).marshal()


def delete(event, context):
    """
    delete removes a key-value item from dynamodb
    :param event:
    :param context:
    :return: LambdaProxyResponse
    """
    try:
        params = event['pathParameters']

        if params is not None and 'id' in params:
            res = table.delete_item(Key={keyName: params['id']}, ReturnValues='ALL_OLD')
            logger.info(res)
            if 'Attributes' not in res or res['Attributes'] == {}:
                return Response(404).marshal()
            return Response(200, body=res['Attributes']).marshal()
        else:
            return Response(400).marshal()

    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(500, error).marshal()


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


class Response(object):
    """
    LambdaProxyResponse object used to return responses more easily
    """
    def __init__(self, statusCode, body=None, headers=None, is_base64_encoded=False):
        if headers is None:
            headers = {}
        if body is None:
            body = {}
        self.statusCode = statusCode
        self.headers = headers
        self.body = body
        self.isBase64Encoded = is_base64_encoded

    def marshal(self):
        """
        marshals Response into json
        :return: string
        """
        return {
            'statusCode': self.statusCode,
            'headers': self.headers,
            'body': json.dumps(self.body, cls=DynamoDBEncoder),
            'isBase64Encoded': self.isBase64Encoded
        }
