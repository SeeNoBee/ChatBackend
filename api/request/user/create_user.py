from marshmallow import fields, post_load

from api.base import RequestDto, SchemaWithPasswordStrength
from api.exceptions import ApiRequestValidationException


class RequestCreateUserDtoSchema(SchemaWithPasswordStrength):
    login = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    secret_word = fields.Str(required=True, allow_none=False)

    # проверяем длину пароля на валидность
    @post_load
    def check_login_password_secret_word_length(self, data: dict, **kwargs):
        if len(data['login']) < 5 or len(data['password']) < 6 or len(data['secret_word']) < 8:
            raise ApiRequestValidationException('Bad request')

        return data


# можно добавить также второго родителя, чтобы IDE знал
# какие в нашей схеме существуют поля
class RequestCreateUserDto(RequestDto, RequestCreateUserDtoSchema):
    __schema__ = RequestCreateUserDtoSchema
