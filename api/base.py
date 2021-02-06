import datetime
import re

from marshmallow import Schema, EXCLUDE, ValidationError, pre_load, post_load

from api.exceptions import ApiRequestValidationException, ApiResponseValidationException


# создание класс DTO (data transfer object) объекта
class RequestDto:
    __schema__: Schema

    def __init__(self, data: dict):
        try:
            valid_data = self.__schema__(unknown=EXCLUDE).load(data)
        except ValidationError as error:
            raise ApiRequestValidationException(error.messages)
        else:
            self._import(valid_data)

    def _import(self, data: dict):
        for name, field in data.items():
            self.set(name, field)

    def set(self, key, value):
        setattr(self, key, value)


# универсальный класс для превращения данных в DTO объект
class ResponseDto:
    __schema__: Schema

    def __init__(self, obj, many: bool = False):

        properties = [self.parse_obj(o) for o in obj] if many else self.parse_obj(obj)

        try:
            self._data = self.__schema__(unknown=EXCLUDE, many=many).load(properties)
        except ValidationError as error:
            raise ApiResponseValidationException(error.messages)

    @staticmethod
    def parse_obj(obj: object):
        properties = {}

        # проходимся по атрибутам объекта и ищем те атрибуты,
        # которые нам нужны (атрибуты из схемы) - превращаем объект из DTO в словарь,
        # чтобы потом отправить клиенту на frontpage
        for prop in dir(obj):
            # выбираем не приватные методы
            if not prop.startswith('_') and not prop.endswith('_'):
                attr = getattr(obj, prop)
                if not callable(attr):
                    properties[prop] = attr

        return properties

    def dump(self) -> dict:
        return self._data


class SchemaWithDateTime(Schema):

    # оба декораторы нужна, чтобы преобразовывать объект из datetime.datetime в str
    # до и после валидации
    @pre_load
    @post_load
    def deserialize_datetime(self, data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = self.datetime_to_iso(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = self.datetime_to_iso(data['updated_at'])

        return data

    @staticmethod
    def datetime_to_iso(date):
        if isinstance(date, datetime.datetime):
            return date.isoformat()
        return date


class SchemaWithPasswordStrength(Schema):
    @post_load
    def check_password_strength(self, data: dict, **kwargs):
        reg = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])')
        result = re.search(reg, data['password'])
        if not result:
            raise ApiRequestValidationException('Bad request')

        return data
