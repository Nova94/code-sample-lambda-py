Code Sample Python Lambda
=========================
This is a code sample focused around crud operations for a dynamodb backed key-value store

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
**Summary:** updates/overrides previously stored key

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

##### ***PUT***
**Summary:** updates/overrides previously stored key

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| value | query |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | Success |
| 400 | Bad Request |
| 415 | Unsupported Media Type |
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
