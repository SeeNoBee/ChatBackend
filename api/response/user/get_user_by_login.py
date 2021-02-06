from marshmallow import fields

from api.base import ResponseDto, SchemaWithDateTime


class ResponseGetUserByLoginDtoSchema(SchemaWithDateTime):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    sent_messages = fields.Int(required=True)
    received_messages = fields.Int(required=True)


class ResponseGetUserByLoginDto(ResponseDto, ResponseGetUserByLoginDtoSchema):
    __schema__ = ResponseGetUserByLoginDtoSchema
