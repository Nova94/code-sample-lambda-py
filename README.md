# code-sample-lambda-py

#### description
This project is a code sample utilizing the following:
    
    - python3.6
    - serverless
    - serverless-python-requirements
    - AWS lambda, API gateway, dynamodb

#### acceptance criteria
Implement the requirements below to create a basic key/value service:
* uses Python
* create a RESTful API using AWS Lambda.
* the route should be something like /key but should be versionable
* show some example uses of the service
* use cases:
    * user should be able to get all keys/values
    * user should be able to get a specific key/value
    * user should be able to add a key/value
    * user should be able to update a key/value
    * user should be able to delete a key/value
* enable a backing store using DynamoDB. 
* The code should be runnable and have some form of demonstration. For example, a user would add a key of 'sports', its value the list of 'baseball', 'hockey' and 'football'.
* The code should have automated tests for all endpoints
* Tests should be written in PyTest
* Share via code repository
* Provide stack deployment script using Serverless framework: https://serverless.com/

Useful Serverless Plugin:
serverless-python-requirements - https://github.com/UnitedIncome/serverless-python-requirements
