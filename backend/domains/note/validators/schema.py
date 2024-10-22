from marshmallow import Schema, fields

# Define a schema for validation
class CreateNoteSchema(Schema):
    title = fields.String(required=True, validate=lambda x: len(x) > 0)
    content = fields.String(required=True)

class UpdateNoteSchema(Schema):
    title = fields.String(required=False, validate=lambda x: len(x) > 0)
    content = fields.String(required=False)