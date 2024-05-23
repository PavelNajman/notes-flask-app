from marshmallow import Schema, fields
from marshmallow.validate import Length


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(max=1024))
    body = fields.Str(required=True, validate=Length(max=8192))
    owner = fields.Int(dump_only=True)
