import json
import decimal
from boto3.dynamodb.types import Decimal, Binary


class DynamoDBEncoder(json.JSONEncoder):
    """
    DynamoDBEncoder encodes python types received from dynamodb into a valid json encoding
    """
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
        elif isinstance(o, bytes):
            return o.decode('utf-8')
        return super(DynamoDBEncoder, self).default(o)


class DynamoDBDecoder(json.JSONDecoder):
    """
    DynamoDBDecoder decodes json and uses an object hook to change float to Decimals
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj):
        for k, v in obj.items():
            if isinstance(v, float):
                obj[k] = Decimal(str(v))
        return obj


class Response(object):
    """
    LambdaProxyResponse object used to return responses more easily
    """
    def __init__(self, status_code, body=None, headers=None, is_base64_encoded=False):
        if headers is None:
            headers = {}
        if body is None:
            body = {}
        self.statusCode = status_code
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
