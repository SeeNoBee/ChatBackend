from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestGetUserByLoginDto
from api.response import ResponseGetUserByLoginDto

from db.database import DBSession
from db.queries import user as user_queries
from db.exceptions import DBUserNotFoundException, DBUserDeletedException

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicUserDeletedException


class GetUserByLoginEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, user_login: str, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            db_user = user_queries.get_user(session=session, user_id=token['id'])
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        # проверяем, что пользователь посылает запрос от своего имени
        if token.get('id') != db_user.id:
            return await self.make_response_json(status=403)

        request_model = RequestGetUserByLoginDto({'login': user_login})

        try:
            user_info = user_queries.get_user(session, login=request_model.login)
        except DBUserNotFoundException:
            raise SanicUserNotFoundException('User not found')
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        response_model = ResponseGetUserByLoginDto(user_info)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200,
        )
