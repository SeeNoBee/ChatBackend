from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseGetUserDto

from db.database import DBSession
from db.exceptions import DBUserDeletedException
from db.queries import user as user_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserDeletedException


class GetUserEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            db_user = user_queries.get_user(session=session, user_id=token['id'])
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        # проверяем, что пользователь посылает запрос от своего имени
        if token.get('id') != db_user.id:
            return await self.make_response_json(status=403)

        db_user = user_queries.get_user(session=session, user_id=token['id'])

        response_model = ResponseGetUserDto(db_user)

        return await self.make_response_json(
            status=200, body=response_model.dump()
        )
