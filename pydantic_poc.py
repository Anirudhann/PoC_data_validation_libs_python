"""
pip install pydantic==1.8.1
"""

from typing import Union, Optional
from pydantic import BaseModel, ValidationError, constr, validator

class AdditionalValidationsModel(BaseModel):

    @validator("fileName", check_fields=False)
    def check_csv_file_format(cls, value):
        if not value[-3:] == "csv":
            raise ValueError('Invalid fileName')
        return value

class UserModel(AdditionalValidationsModel):
    name: constr(min_length=0, max_length=30, strict=True, strip_whitespace=True, regex="^[a-zA-Z0-9'-]+$")
    role: constr(min_length=0, max_length=20, strict=True, strip_whitespace=True, regex="(Dev|Test|Support)") #check
    referenceId: constr(min_length=0, max_length=30, strict=True, strip_whitespace=True, regex="^[a-zA-Z0-9 '-]+$")
    postalcode: constr(min_length=5, max_length=10, strict=True, strip_whitespace=True, regex="^\d{5}\-\d{4}$|^\d{5}$")
    payload: Optional[Union[str, dict]]

class FileModel(UserModel):
    fileName: constr(min_length=0, max_length=100, strict=True, strip_whitespace=True, regex="^[a-zA-Z0-9 '-_.]+$")

request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "11234",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachment.csv"
}


try:
    FileModel(**request)
    print("All validations success")
except ValidationError as e:
    validation_error = {}
    for k in e.errors():
        validation_error[k['loc'][0]] = {'msg':k['msg'], 'type':k['type']}
    print(validation_error)