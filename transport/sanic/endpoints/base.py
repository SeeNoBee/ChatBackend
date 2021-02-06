# базовый класс для уровня endpoint'ов

from sanic.request import Request
from sanic.response import BaseHTTPResponse
from sanic.exceptions import SanicException

from transport.sanic.base import SanicEndpoint


class BaseEndpoint(SanicEndpoint):

    # метод будет определять тип запросы и вызывать соответствующую функцию
    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:

        # получаем объект database
        database = self.context.database
        session = database.make_session()

        # проводим обработку ошибок валидации в любом методе
        try:
            # с помощью super() вызываем метод, прописанный в классе-родителе (SanicEndpoint)
            return await super()._method(request, body, session, *args, **kwargs)
        except SanicException as error:
            return await self.make_response_json(status=error.status_code, message=str(error))
