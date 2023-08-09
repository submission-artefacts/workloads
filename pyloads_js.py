import json
import random
import string

js_payloads = {
    "wage-insert": [
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
            "role": "staff",
            "base": 3000,
            "merit": 2000,
            "operator": 1
        },
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=25)),
            "role": "staff",
            "base": 30000,
            "merit": 20000,
            "operator": 1
        },
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=50)),
            "role": "staff",
            "base": 300000,
            "merit": 200000,
            "operator": 1
        }
    ],
    "wage-format": [
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
            "role": "staff",
            "base": 3000,
            "merit": 2000,
            "operator": 1
        },
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=25)),
            "role": "staff",
            "base": 30000,
            "merit": 20000,
            "operator": 1
        },
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=50)),
            "role": "staff",
            "base": 300000,
            "merit": 200000,
            "operator": 1
        }
    ],
    "wage-db-writer": [
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=5)),
            "COUCHDB_URL": "http://couch_user:couch_password@wsk-host:5984",
            "realpay": 4806.5,
            "total": 6500,
            "base": 3000,
            "operator": 1,
            "merit": 2000,
            "INSURANCE": 1500,
            "COUCHDB_DATABASE": "wage"
        },
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=25)),
            "COUCHDB_URL": "http://couch_user:couch_password@wsk-host:5984",
            "realpay": 48065,
            "total": 51500,
            "base": 30000,
            "operator": 1,
            "merit": 20000,
            "INSURANCE": 1500,
            "COUCHDB_DATABASE": "wage"
        },
        {
            "id": random.randint(0, 9999),
            "name": ''.join(random.choices(string.ascii_lowercase + string.digits, k=50)),
            "COUCHDB_URL": "http://couch_user:couch_password@wsk-host:5984",
            "realpay": 480650,
            "total": 501500,
            "base": 300000,
            "operator": 1,
            "merit": 200000,
            "INSURANCE": 1500,
            "COUCHDB_DATABASE": "wage"
        }
    ]
}
