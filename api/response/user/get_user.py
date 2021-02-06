from marshmallow import fields

from api.base import ResponseDto, SchemaWithDateTime


class ResponseGetUserDtoSchema(SchemaWithDateTime):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    sent_messages = fields.Int(required=True)
    received_messages = fields.Int(required=True)


class ResponseGetUserDto(ResponseDto, ResponseGetUserDtoSchema):
    __schema__ = ResponseGetUserDtoSchema
