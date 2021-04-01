"""
pip install marshmellow==3.11.1
"""

import re
from marshmallow import Schema, fields, ValidationError, validate, pre_load

class PayloadField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, dict):
            return value
        else:
            raise ValidationError('Field should be str or dict')

class PostalcodeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if re.compile(r"^\d{5}\-\d{4}$|^\d{5}$").search(value):
            return value
        else:
            raise ValidationError('Invalid postalcode')

class FilenameField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if value[-3:] == "csv":
            return value
        else:
            raise ValidationError('Invalid fileName')

class UserSchema(Schema):
    name = fields.String(validate=validate.Length(min=0, max=30), required=True)
    role = fields.String(validate=[validate.Length(min=0, max=30), validate.OneOf(['Dev', 'Test', 'Support'])], required=True)
    referenceId = fields.String(validate=validate.Length(min=0, max=30), required=True)
    postalcode = PostalcodeField(validate=validate.Length(min=5, max=10), required=True)
    payload = PayloadField(validate=validate.Length(min=0, max=1000))
    fileName = FilenameField(validate=validate.Length(min=0, max=30), required=True)

    @pre_load
    def remove_spl_char(self, in_data, **kwargs):
        in_data["name"] = in_data["name"].translate(str.maketrans('', '', "\'- "))
        in_data["role"]  = in_data["role"].translate(str.maketrans('', '', "\'- "))
        in_data["referenceId"] = in_data["referenceId"].translate(str.maketrans('', '', "\'- "))
        in_data["postalcode"] = in_data["postalcode"].replace(" ", "")
        in_data["payload"] = in_data["postalcode"].replace(" ", "")
        in_data["fileName"] = in_data["fileName"].translate(str.maketrans('', '', "\'-_. "))
        return in_data

request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "11234",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachment.csv"
}

try:
    result = UserSchema().load(request)
    print("All validations success")
except ValidationError as err:
    print(err.messages)