"""
pip install jsonschema==3.2.0
"""

import ast
import json
import jsonschema

def user_model(input_request):

    BaseVal = jsonschema.Draft7Validator

    #Build a new type checker for payload
    def is_payload(checker, inst):
        try:
            return isinstance(json.loads(input_request["payload"]), dict)
        except Exception:
            return False

    #Build a new type checker for filename
    def is_filename(checker, inst):
        if not input_request["payload"][-3:] == "csv":
            return False
        return True

    payload_check = BaseVal.TYPE_CHECKER.redefine('payload', is_payload)
    user_model = jsonschema.validators.extend(BaseVal, type_checker=payload_check)
    filename_check = user_model.TYPE_CHECKER.redefine('fileName', is_filename)
    user_model = jsonschema.validators.extend(user_model, type_checker=filename_check)

    user_schema = {
        "user_details":{
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "pattern": "[a-zA-Z0-9'-]$",
                    "minLength": 0,
                    "maxLength": 30,
                    "error_msg": "{'role': 'Invalid name'}"
                    },
                "role": {
                    "type": "string",
                    "enum": ['Dev', 'Test', 'Support'],
                    "minLength": 0,
                    "maxLength": 20,
                    "error_msg": "{'role': 'Invalid role'}"
                },
                "referenceId": {
                    "type": "string",
                    "pattern": "[a-zA-Z0-9 '-]$",
                    "minLength": 0,
                    "maxLength": 30,
                    "error_msg": "{'role': 'Invalid referenceId'}"
                    },
                "postalcode": {
                    "type": "string",
                    "pattern": "^\d{5}\-\d{4}$|^\d{5}$",
                    "minLength": 5,
                    "maxLength": 10,
                    "error_msg": "{'postal code': 'Invalid postalcode'}"
                    },
                "payload": {
                    "type": "payload",
                    "minLength": 0,
                    "maxLength": 1000,
                    "error_msg": "{'payload': 'Invalid payload'}"
                    },
                "fileName": {
                    "type": "string",
                    "pattern": "[a-zA-Z0-9 '-_.]$",
                    "minLength": 0,
                    "maxLength": 100,
                    "error_msg": "{'payload': 'Invalid fileName'}"
                    },
                },
            "required": [
                "name",
                "role",
                "referenceId",
                "postalcode",
                "fileName",
            ],
        }
    }
    user = user_model(user_schema.get("user_details"))

    validation_error ={}
    for err in user.iter_errors(input_request):
        try:
            validation_error.update(ast.literal_eval(err.schema['error_msg']))
        except KeyError:
            field = err.message.split( ' ', 1)[0].replace("'", "")
            error_msg = field + " is required"
            validation_error.update({field:error_msg})

    if validation_error:
        return False, validation_error

    return True, None

request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "12345",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachments.csv"
}

result, error = user_model(request)
if not result:
    print(error)
else:
    print("All validations success")
