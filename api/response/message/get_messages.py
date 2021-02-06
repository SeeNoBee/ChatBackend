from marshmallow import fields

from api.base import ResponseDto, SchemaWithDateTime


class ResponseGetMessageDtoSchema(SchemaWithDateTime):
    id = fields.Int(required=True)
    sender_id = fields.Int(required=True)
    recipient_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    message = fields.Str(required=True, allow_none=False)
    is_read = fields.Boolean()


class ResponseGetMessageDto(ResponseDto, ResponseGetMessageDtoSchema):
    __schema__ = ResponseGetMessageDtoSchema
