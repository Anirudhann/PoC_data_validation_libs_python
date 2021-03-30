"""
pip install schema==0.7.4
"""

from schema import Schema, And, Use, Optional, Regex, Or
import json

def user_model(input_request):

    user_schema= Schema({
        "name": And(Regex("^[a-zA-Z0-9 '-]{0,30}$"), error="Invalid name"),
        "role": And(Or('Dev', 'Test', 'Support'), error = "Invalid role"),
        "referenceId": And(Regex("^[a-zA-Z0-9 '-]{0,30}$"), error="Invalid referenceId"),
        "postalcode":And(Regex("^\d{5}\-\d{4}$|^\d{5}$"), error = "Invalid postalcode"),
        Optional("payload"):Use(json.loads, error = "Invalid payload"),
        "fileName": And(Regex("^[a-zA-Z0-9 '-_.]{0,100}$"), Use(str), lambda f: True if f[-3:]=="csv" else False, error="Invalid fileName"),
        },
        ignore_extra_keys = True
    )

    try:
        user_schema.validate(input_request)
        return True, None
    except Exception as e:
        return False, e.code



request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "12345",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachment.csv"
}

result, error = user_model(request)
if not result:
    print(error)
else:
    print("All validations success")