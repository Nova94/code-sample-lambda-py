# code sample lambda py
##### _also known as Lambda+Python K-V store example_
This project builds a serverless K-V store using AWS APIGateway, Lambda, and DynamoDB.

## Getting Started

### Prerequisites

The following should be installed before building the project.

* python 3.6.5 
* [awscli](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* [serverless](https://serverless.com/framework/docs/getting-started/) >=1.12.0 <2.0.0 
* [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements#install)

## Installation

Install package dependencies with.

```
$ pip install -r requirements.txt
```

## Deployment

deploy with `make`  (runs unit tests first) or `make deploy` - it will deploy a cloudformation stack using serverless

example output _(don't worry this stack no longer exists...)_
```
Service Information
service: code-sample-lambda-py
stage: dev
region: us-west-2
stack: code-sample-lambda-py-dev
api keys:
  test-key: yzd6JQJGN9Di4Q2t9jlB6TgUFSF2E7k7zd8lziz2
endpoints:
  GET - https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys
  GET - https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/{id}
  POST - https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys
  PUT - https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys
  PUT - https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/{id}
  DELETE - https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/{id}
functions:
  kvGet: code-sample-lambda-py-dev-kvGet
  kvCreate: code-sample-lambda-py-dev-kvCreate
  kvUpdate: code-sample-lambda-py-dev-kvUpdate
  kvDelete: code-sample-lambda-py-dev-kvDelete

Stack Outputs
UsersTableArn: arn:aws:dynamodb:us-west-2:271741776246:table/dev-code-sample-lambda-py-kv
KvGetLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:271741776246:function:code-sample-lambda-py-dev-kvGet:29
KvDeleteLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:271741776246:function:code-sample-lambda-py-dev-kvDelete:27
KvUpdateLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:271741776246:function:code-sample-lambda-py-dev-kvUpdate:27
ServiceEndpoint: https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev
ServerlessDeploymentBucketName: code-sample-lambda-py-de-serverlessdeploymentbuck-1rxqoz4dti45m
KvCreateLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:271741776246:function:code-sample-lambda-py-dev-kvCreate:27
```

`$ make remove` - destroys the cloudformation stack

## Running the tests

Run `$ make test` for unit tests

Run the following command after a deploy to run through acceptance tests/demo.
Service Endpoint and test-key are outputted during the deploy phase. 
```
$ make acceptance endpoint={Service Endpoint} apikey={test-key}

example
$ make acceptance endpoint=https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev apikey=Bwdy2iIYHR4xPj3VEfvFl6YqMKytUBY15HIsGTe3
``` 

example output
```
acceptance.py 
testing POST /api/v1/keys
POST 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys json response {'errors': []}
testing GET /api/v1/keys/{id}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_string json response {'Id': 'key_string', 'Value': 'hello world!'}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_integer json response {'Id': 'key_integer', 'Value': 123}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_float json response {'Id': 'key_float', 'Value': 123.45}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_bytes json response {'Id': 'key_bytes', 'Value': '8 bytes walk into a bar, the bartenders asks "What will it be?" One of them says, "Make us a double."'}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_bool json response {'Id': 'key_bool', 'Value': False}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_list json response {'Id': 'key_list', 'Value': ['funny', 'joke', 'here']}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_set json response {'Id': 'key_set', 'Value': [1]}
GET 200 https://gvzb8hkoc1.execute-api.us-west-2.amazonaws.com/dev/api/v1/keys/key_object json response {'Id': 'key_object', 'Value': {'key_integer': 123, 'key_float': 123.45, 'key_string': 'hello world!', 'key_list': ['funny', 'joke', 'here'], 'key_bytes': '8 bytes walk into a bar, the bartenders asks "What will it be?" One of them says, "Make us a double."', 'key_set': [1], 'key_bool': False, 'key_recursion': True}}
```

## Built With

* [boto3](http://boto3.readthedocs.io/en/latest/index.html) - The AWS SDK for python
* [pip](https://pypi.org/project/pip/) - Dependency Management
* [pytest](https://docs.pytest.org/en/latest/) - Testing Framework

## Contributing

Not really open for contributing at this time. It is just a code sample for people to look at.

## Authors
* **[Lisa Gray](linkedin.com/in/gray7)** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
