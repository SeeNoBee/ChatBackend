from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response.user.auth_user import ResponseAuthUserDto, AuthResponseObject
from db.database import DBSession

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import (
    SanicUserNotFoundException, SanicPasswordHashException, SanicUserDeletedException
)

from api.request import RequestAuthUserDto

from db.queries import user as user_queries
from db.exceptions import DBUserNotFoundException, DBUserDeletedException

from utils.password import check_hash, CheckPasswordHashException

from utils.auth import create_token


# endpoint для авторизации юзера
class AuthUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestAuthUserDto(body)

        try:
            # процесс идентификации пользователя
            db_user = user_queries.get_user(session, login=request_model.login)
        except DBUserNotFoundException:
            raise SanicUserNotFoundException('User not found')
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        try:
            check_hash(request_model.password, db_user.password)
        except CheckPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'id': db_user.id,
        }

        token = create_token(payload)
        response = AuthResponseObject(token)

        response_model = ResponseAuthUserDto(response)

        return await self.make_response_json(body=response_model.dump(), status=200)
