# demonstration / acceptance tests of service

import requests
import json
from helpers import DynamoDBEncoder
from os import environ

URI = environ["SERVICE_ENDPOINT"]
API_KEY = environ["API_KEY"]

BASE_PATH = "/api/v1"


def test_api():
    headers = {'X-API-KEY': API_KEY, 'Accept': 'application/json'}
    items = {
        'key_string': 'hello world!',
        'key_integer': 123,
        'key_float': 123.45,
        'key_bytes': b'8 bytes walk into a bar, the bartenders asks \"What will it be?\" '
                     b'One of them says, "Make us a double."',
        'key_bool': False,
        'key_list': ['funny', 'joke', 'here'],
        'key_set': {1, 1},  # There can be only one!
        'key_object': {
            'key_recursion': True,
            'key_string': 'hello world!',
            'key_integer': 123,
            'key_float': 123.45,
            'key_bytes': b'8 bytes walk into a bar, the bartenders asks \"What will it be?\" '
                         b'One of them says, "Make us a double."',
            'key_bool': False,
            'key_list': ['funny', 'joke', 'here'],
            'key_set': {1, 1}  # There can be only one!
        }
    }
    # add a k-v items using /create
    r = requests.post(f"{URI+BASE_PATH}/keys", data=json.dumps(items, cls=DynamoDBEncoder), headers=headers)
    print(f'POST {r.status_code} {r.url} json response {r.json()}')

    print(f"testing GET {BASE_PATH}/keys/" + "{id}")
    for k, v in items.items():
        r = requests.get(f"{URI+BASE_PATH}/keys/{k}", headers=headers)
        print(f'GET {r.status_code} {r.url} json response {r.json()}')

    print(f"testing GET {BASE_PATH}/keys")
    r = requests.get(f"{URI+BASE_PATH}/keys", headers=headers)
    print(f'GET {r.status_code} {r.url} json response {r.json()}')

    print(f"testing PUT {BASE_PATH}/keys/" + '{id}')
    for k, v in items.items():
        r = requests.put(f"{URI+BASE_PATH}/keys/{k}", params={'value': 'update'}, headers=headers)
        print(f'PUT {r.status_code} {r.url} json response {r.json()}')

    r = requests.get(f"{URI+BASE_PATH}/keys", headers=headers)
    print(f'GET {r.status_code} {r.url} json response {r.json()}')

    r = requests.put(f"{URI+BASE_PATH}/keys", data=json.dumps({k: 'batch_update' for k in items.keys()}),
                     headers=headers)
    print(f'PUT {r.status_code} {r.url} json response {r.json()}')

    r = requests.get(f"{URI+BASE_PATH}/keys", headers=headers)
    print(f'GET {r.status_code} {r.url} json response {r.json()}')

    for k, v in items.items():
        r = requests.delete(f"{URI+BASE_PATH}/keys/{k}", headers=headers)
        print(f'DELETE {r.status_code} {r.url} json response {r.json()}')

    r = requests.get(f"{URI+BASE_PATH}/keys", headers=headers)
    print(f'GET {r.status_code} {r.url} json response {r.json()}')
