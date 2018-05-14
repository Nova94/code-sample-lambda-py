# code-sample-lambda-py

#### description
This project is a code sample utilizing the following:
    
    - python3.6
    - serverless
    - serverless-python-requirements
    - AWS lambda, API gateway, dynamodb, cloudformation
    

#### example usages

#### dynamodb

The following defines the schema of the dynamodb table:
```yaml
TableName: ${self:provider.stage}-${self:service}-kv
AttributeDefinitions:
  - AttributeName: 'Key'
    AttributeType: S
KeySchema:
  - AttributeName: 'Key'
    KeyType: HASH
ProvisionedThroughput:
  ReadCapacityUnits: 1
  WriteCapacityUnits: 1
TimeToLiveSpecification:
  AttributeName: 'Expires'
  Enabled: true
```

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

# swagger api

**Version:** 1.0

**Contact information:**  
graylisa94@gmail.com  

### /keys
---
##### ***POST***
**Summary:** Create a new key value item(s) in dynamodb

**Description:** this endpoint called with of k-v in json, each k-v translates to item in dynamo

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 400 | Bad Request |
| 415 | Unsupported Media Type |
| 500 | Internal Server Error |

##### ***PUT***
**Summary:** updates/overrides perviously stored key

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 400 | Bad Request |
| 415 | Unsupported Media Type |
| 500 | Internal Server Error |

##### ***GET***
**Summary:** get items from dynamodb

**Description:** this endpoint called without {id} returns all items in dynamodb (until 1MB reached)

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 500 | Internal Server Error |

### /keys/{id}
---
##### ***GET***
**Summary:** get item(s) from dynamodb

**Description:** this endpoint called with {id} parameter returns item matching id

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 404 | Not Found |
| 500 | Internal Server Error |

##### ***DELETE***
**Summary:** removes key-value item from dynamodb

**Description:** deletes the key-value item matching {id} path parameter and returns the attributes if found

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 404 | Not Found |
| 500 | Internal Server Error |

