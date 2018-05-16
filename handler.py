import boto3
import logging
import json
from os import environ
from botocore.exceptions import ClientError
from http import HTTPStatus as hStat
from helpers import Response, DynamoDBDecoder

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
                return Response(hStat.OK, item['Item']).marshal()
            else:
                return Response(hStat.NOT_FOUND).marshal()

        # TODO: handle when >1MB returned.
        items = table.scan()
        logger.info(items['Items'])
        return Response(hStat.OK, items['Items']).marshal()
    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(hStat.INTERNAL_SERVER_ERROR, error).marshal()


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
            return Response(hStat.UNSUPPORTED_MEDIA_TYPE).marshal()

    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(hStat.INTERNAL_SERVER_ERROR, error).marshal()
    except TypeError as e:
        logger.error(e)
        return Response(hStat.BAD_REQUEST, 'Bad Request').marshal()


def update(event, context):
    errors = []
    try:
        p_params = event["pathParameters"]
        q_params = event["queryStringParameters"]
        return update_items(errors, event, p_params, q_params)

    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(hStat.INTERNAL_SERVER_ERROR, error).marshal()
    except TypeError as e:
        logger.error(e)
        return Response(hStat.BAD_REQUEST, 'Bad Request').marshal()


def update_items(errors, event, p_params, q_params):
    if p_params is not None and q_params is not None and 'id' in p_params and 'value' in q_params:
        res = table.put_item(Item={keyName: p_params['id'], 'Value': q_params['value']},
                             ExpressionAttributeValues={':id_val': p_params['id']},
                             ConditionExpression=f"contains(Id, :id_val)")
        logger.info(res)
        return Response(hStat.OK).marshal()
    elif 'headers' in event and 'Accept' in event['headers'] and event['headers']['Accept'] == 'application/json':
        return put_items_from_body(errors, event)
    else:
        unaccept_content_type = Response(hStat.UNSUPPORTED_MEDIA_TYPE, {
            "errors": "please use path/query param combo or application/json"}).marshal()
        logger.error(unaccept_content_type)
        return unaccept_content_type


def put_items_from_body(errors, event):
    """
    puts k-v items from body into dynamodb
    :param errors:
    :param event:
    :param log:
    :return: LambdaProxyResponse
    """
    if event['body'] is not None:
        body = json.loads(event['body'], cls=DynamoDBDecoder)
        with table.batch_writer() as batch:
            try:
                for k, v in body.items():
                    res = batch.put_item(Item={keyName: k, 'Value': v})
                    logger.info(res)
            except ClientError as e:
                error = json.dumps(e.response['Error'])
                logger.error(error)
                errors.append(error)
            except TypeError:
                raise TypeError(errors)

        return Response(hStat.OK, {'errors': errors}).marshal()
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
                return Response(hStat.NOT_FOUND).marshal()
            return Response(hStat.OK, body=res['Attributes']).marshal()
        else:
            return Response(hStat.BAD_REQUEST).marshal()

    except ClientError as e:
        error = e.response['Error']
        logger.error(error)
        return Response(hStat.INTERNAL_SERVER_ERROR, error).marshal()
