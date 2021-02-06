from marshmallow import Schema, fields

from api.base import RequestDto


class RequestRestoreUserDtoSchema(Schema):
    login = fields.Str(required=True, allow_none=False)


class RequestRestoreUserDto(RequestDto, RequestRestoreUserDtoSchema):
    __schema__ = RequestRestoreUserDtoSchema
