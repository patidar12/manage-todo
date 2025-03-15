from marshmallow import Schema, EXCLUDE

class BaseValidatorSchema(Schema):
    class Meta:
        unknown = EXCLUDE
