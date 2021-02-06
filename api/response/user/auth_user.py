from sanic.exceptions import SanicException

from api.base import ResponseDto


# ошибка валидации - неверный запрос
class ValidationError(SanicException):
    status_code = 400


# реализуем собственную схему для валидации авторизации (токена)
class ResponseAuthUserDtoSchema:

    def __init__(self, *args, **kwargs):
        self.fields = {'Authorization': ''}
        self.data = {}

    def load(self, data: dict) -> dict:
        for key, value in data.items():
            if key not in self.fields:
                continue
            if not isinstance(value, self.fields[key].__class__):
                raise ValidationError(f'{key} should be str')

            self.data[key] = value

        return self.data


class ResponseAuthUserDto(ResponseDto):
    __schema__ = ResponseAuthUserDtoSchema


# формируем объект для ответа
class AuthResponseObject:
    def __init__(self, token):
        self.Authorization = token
