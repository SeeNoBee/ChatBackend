from marshmallow import fields

from api.base import ResponseDto, SchemaWithDateTime


class ResponseGetCreatedMessageDtoSchema(SchemaWithDateTime):
    id = fields.Int(required=True)
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)
    created_at = fields.Str(required=True)
    updated_at = fields.DateTime(required=True)
    message = fields.Str(required=True, allow_none=False)


class ResponseGetCreatedMessageDto(ResponseDto, ResponseGetCreatedMessageDtoSchema):
    __schema__ = ResponseGetCreatedMessageDtoSchema
