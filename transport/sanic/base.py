# базовый модуль для эндпоинтов

from http import HTTPStatus
from typing import Iterable

from sanic.request import Request
from sanic.response import BaseHTTPResponse, json

from configs.config import ApplicationConfig
from context import Context
from transport.sanic.exceptions import SanicAuthException
from utils.auth import read_token, ReadTokenException
from db.database import DBSession


class SanicEndpoint:

    # чтобы сделать будущим экземпляр этого класса вызываемым
    async def __call__(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        # проверка нужна ли аутентификация
        if self.auth_required:
            try:
                token = {
                    'token': self.import_body_auth(request)
                }
            except SanicAuthException as error:
                return await self.make_response_json(status=error.status_code, message=str(error))
            else:
                kwargs.update(token)

        return await self.handler(request, *args, **kwargs)

    def __init__(
            self,
            config: ApplicationConfig,
            context: Context,
            uri: str,
            methods: Iterable,
            # флаг для определения нужна ли для метода авторизация
            auth_required: bool = False,
            *args, **kwargs
    ):
        self.config = config
        self.uri = uri
        self.methods = methods
        self.context = context
        self.auth_required = auth_required
        # для того, чтобы при наследовании этого класса классом потомком
        # получать название класса потомка, а не родителя
        self.__name__ = self.__class__.__name__

    # метод для формирования ответа
    @staticmethod
    async def make_response_json(
            body: dict = None, status: int = 200, message: str = None, error_code: int = None
    ) -> BaseHTTPResponse:

        # проверка если мы не передали ничего в качестве тела запроса
        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase,  # текстовое обозначение статуса (200 = OK)
                'status': error_code or status,  # если не указан error_code, то возьмем код из status
            }

        return json(body=body, status=status)

    # обработчик json
    @staticmethod
    def import_body_json(request: Request) -> dict:
        # проверяем, что в типе запроса существует application/json
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    # получение заголовков
    @staticmethod
    def import_body_headers(request: Request) -> dict:
        headers = {
            header: value
            for header, value in request.headers.items()
            if header.lower().startswith('x-')
        }

        return headers

    # если в реквесте есть токен, то получает его и добавляет в body данные о том кто авторизован
    @staticmethod
    def import_body_auth(request: Request) -> dict:
        # получаем токен из заголовка запроса
        token = request.headers.get('Authorization')
        try:
            return read_token(token)
        except ReadTokenException as error:
            raise SanicAuthException(str(error))

    # обработка запроса
    async def handler(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        body = {}

        body.update(self.import_body_json(request))
        body.update(self.import_body_headers(request))

        return await self._method(request, body, *args, **kwargs)

    # приватный метод, который не требуется использовать снаружи
    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        # определяем тип запроса (POST, GET)
        method = request.method.lower()
        func_name = f'method_{method}'

        # проверка на наличие метода для данного типа запроса
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_implemented(method=method)

    # для методов, которые еще не реализованы
    async def method_not_implemented(self, method: str) -> BaseHTTPResponse:
        return await self.make_response_json(status=500, message=f'Method {method.upper()} not implemented yet')

    async def method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='GET')

    async def method_post(self, request: Request, session: DBSession, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='POST')

    async def method_patch(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='PATCH')

    async def method_delete(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='DELETE')
