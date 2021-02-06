# редактирование сообщений

from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchMessageDtoSchema(Schema):
    message = fields.Str(required=True, allow_none=False)


class RequestPatchMessageDto(RequestDto, RequestPatchMessageDtoSchema):
    __schema__ = RequestPatchMessageDtoSchema
