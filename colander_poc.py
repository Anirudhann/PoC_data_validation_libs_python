"""
pip install cerberus==1.8.3
"""
import colander
import json
import re

# regex to match US zip code format
postalcode_regex = re.compile(
    r"^\d{5}\-\d{4}$|^\d{5}$"
)

request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "12345",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachments.csv"
}

prepare_name = lambda x: x.translate(str.maketrans('', '', "\'- "))
prepare_role = lambda x: x.translate(str.maketrans('', '', "\'- "))
prepare_referenceId = lambda x: x.translate(str.maketrans('', '', "\'- "))
prepare_postalcode = lambda x: x.replace(" ", "")
prepare_payload = lambda x: x.replace(" ", "")
prepare_fileName = lambda x: x.translate(str.maketrans('', '', "\'-_. "))

def postalcode_validator(node, kw):
    def validator(node, value):
        if not postalcode_regex.search(kw):
            raise colander.Invalid(
                node, u'Invalid postal code'
            )
    return validator(node,kw)

def payload_validator(node, kw):
    def validator(node, value):
        if not kw and isinstance(json.loads(kw), dict):
            raise colander.Invalid(
                node, u'Invalid Payload'
            )

    return validator(node, kw)


class UserSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), preparer=prepare_name, validator=colander.Length(0, 30))
    role = colander.SchemaNode(colander.String(), preparer=prepare_role,
                                          validator=colander.OneOf(['Dev', 'Test', 'Support']))
    referenceId = colander.SchemaNode(colander.String(), validator=colander.Length(0, 30))
    postalcode = colander.SchemaNode(colander.String(), preparer=prepare_postalcode, validator=colander.All(colander.Length(5,10),postalcode_validator))
    payload = colander.SchemaNode(colander.String(), preparer=prepare_payload, validator=colander.All(colander.Length(0,1000),payload_validator))

def csv_validator(node, kw):
    def validator(node, value):
        if kw[-3:] != "csv" and kw.isalnum():
            raise colander.Invalid(
                node, u'Invalid csv file'
            )
    return validator(node, kw)

class FileSchema(UserSchema):
    fileName = colander.SchemaNode(colander.String(),preparer=prepare_fileName,validator=colander.All(colander.Length(0,100),csv_validator))

schema = FileSchema().bind(request=request)


try:
    schema.deserialize(request)
    print("All validations success")
except colander.Invalid as e:
    errors = e.asdict()
    print(errors)