from marshmallow import Schema, fields

from api.base import RequestDto


class RequestGetUserByLoginDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)


class RequestGetUserByLoginDto(RequestDto, RequestGetUserByLoginDtoSchema):
    __schema__ = RequestGetUserByLoginDtoSchema
