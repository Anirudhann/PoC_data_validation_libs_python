"""
pip install cerberus==1.3.2
"""
import cerberus

user_schema = {
    'name': {'type': 'string', "splchar": ["'", "-"], "check_with": "isalpha", 'minlength': 0,
                          'maxlength': 30, 'required': True},
    'role': {'type': 'string', "splchar": [" ", "'", "-"], 'minlength': 0,
                   'maxlength': 20, 'allowed': ['Dev', 'Test', 'Support'], 'required': True},
    'referenceId': {'type': 'string', "splchar": [" ", "'", "-"], "check_with": "isalnum", 'minlength': 0,
                    'maxlength': 30, 'required': True},
    'postalcode': {'type': 'string', "splchar": ["-", ""], "check_with": "isdigit", 'minlength': 5,
                     'maxlength': 10, 'required': True},
    'payload': {'type': ['dict', 'string'], 'allow_unknown': True, },
    'fileName': {'type': 'string', "splchar": [" ", "'", "-", "_", "."], "check_with": ["csvfile", "isalnum"],
                     'minlength': 0, 'maxlength': 100, 'required': True},
}

class user_model(cerberus.Validator):

    def _validate_splchar(self, splchar, field, value):
        """Remove the special char of a value.
        The rule's arguments are validated against this schema:
        {'type': 'list'}
        """
        self.updated_value = value
        for spl_chars in splchar:
            self.updated_value = self.updated_value.replace(spl_chars, "")

    def _check_with_isalnum(self, field, value):
        """ Test the alnum of a value.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if not self.updated_value.isalnum():
            self._error("Invalid", field)

    def _check_with_isalpha(self, field, value):
        """ Test the alpha of a value.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if not self.updated_value.isalpha():
            self._error("Invalid", field)

    def _check_with_isdigit(self, field, value):
        """ Test the alpha of a value.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if not self.updated_value.isdigit():
            self._error("Invalid", field)

    def _check_with_csvfile(self, field, value):
        """ Test the csvfile.
        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if not self.updated_value[-3:] == "csv":
            self._error("Invalid", field)
        else:
            self.updated_value = self.updated_value[-3:]

request = {
    "name": "John",
    "role": "Dev",
    "referenceId": "reference123",
    "postalcode": "12345",
    "payload": "{\"phone_number\": \"9876543210\", \"email\": \"abcd@xyz.com\", \"date\": \"2001-01-01\"}",
    "fileName": "attachments.csv"
}

user = user_model(user_schema)

if not user.validate(request):
    error = {**user.errors}
    print(error)
else:
    print("All validations success")
