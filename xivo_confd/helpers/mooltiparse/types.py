import collections

from errors import ValidationError


class FieldType(object):

    error_message = "'{value}' is wrong type"
    type_class = None

    def validate(self, value):
        if value is None:
            return
        if not isinstance(value, self.type_class):
            self.raise_error(value)

    def raise_error(self, value):
        msg = self.error_message.format(value=value)
        raise ValidationError(msg)


class Int(FieldType):

    type_class = int
    error_message = "wrong type. Should be an integer"

    def validate(self, value):
        if isinstance(value, bool):
            self.raise_error(value)
        super(Int, self).validate(value)


class Boolean(FieldType):

    type_class = bool
    error_message = "wrong type. Should be a boolean"


class Unicode(FieldType):

    type_class = unicode
    error_message = "wrong type. Should be a unicode string"


class Float(FieldType):

    type_class = float
    error_message = "wrong type. Should be a floating-point number"


class Array(FieldType):

    error_message = "wrong type. Should be an array-like sequence'"

    def __init__(self, field_type, *validators):
        self.field_type = field_type
        self.validators = validators

    def validate(self, value):
        if value is None:
            return
        if not isinstance(value, collections.Iterable):
            self.raise_error(value)
        for element in value:
            self.field_type.validate(element)
            for validator in self.validators:
                validator(element)
