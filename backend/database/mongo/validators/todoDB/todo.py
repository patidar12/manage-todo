from marshmallow import Schema, fields

class ToDoSchema(Schema):
    title = fields.Str()
    description = fields.Str()
