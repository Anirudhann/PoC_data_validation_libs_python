"""
pip install voluptuous==0.12.1
"""

import json
from voluptuous import Required, All, Length, Schema, MultipleInvalid, Invalid, In, Match, truth, Strip

@truth
def payload_validation(value):
    try:
        return isinstance(json.loads(value), dict)
    except Exception:
        raise Invalid("Invalid payload")

@truth
def filename_validation(value):
    if not value[-3:] == "csv":
        return False
    return True

base_model = Schema({
    Required('name'): All(Strip, str, Match("[a-zA-Z0-9 '-]+$"), Length(min=0, max=30), msg="Invalid contactId"),
    Required('role'): All(Strip, str, In(['Dev', 'Test', 'Support'], msg ="Invalid role")),
    Required('referenceId'): All(Strip, str, Match("[a-zA-Z0-9 '-]+$"), Length(min=0,max=30), msg = "Invalid referenceId"),
    Required('postalcode'): All(Strip, str, Match("^\d{5}\-\d{4}$|^\d{5}$"), Length(min=5,max=10), msg = "Invalid postalcode"),
    'payload': All(Strip, payload_validation, Length(min=0,max=1000), msg = "Invalid payload"),
    },
    extra = True
)

user_model = base_model.extend({
    Required('fileName'): All(Strip, str, Match("^[a-zA-Z0-9 '-_.]+$"), filename_validation, Length(min=0,max=100), msg = "Invalid fileName"),
})


request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "12345",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachments.csv"
}

try:
    user_model(request)
    print("All validations success")
except MultipleInvalid as e:
    validation_error = {}
    for i in e.errors:
        field = str(i.path[0])
        error_msg = (field + " is required") if ('required key' in i.msg) else i.msg
        validation_error.update({field: error_msg})
    print(validation_error)