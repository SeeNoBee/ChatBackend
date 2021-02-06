from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchUserPasswordDto

from db.database import DBSession
from db.exceptions import DBIntegrityException, DBDataException, DBUserDeletedException
from db.queries import user as user_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserDeletedException, SanicPasswordHashException, \
    SanicSecretWordHashException

from utils.password import generate_hash, GeneratePasswordHashException, check_hash, CheckPasswordHashException


class ChangePasswordEndpoint(BaseEndpoint):

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, user_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        # проверяем, что пользователь посылает запрос от своего имени
        if token['id'] != user_id:
            return await self.make_response_json(status=403)

        request_model = RequestPatchUserPasswordDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
        except GeneratePasswordHashException as error:
            raise SanicPasswordHashException(str(error))

        # проверка, что пользователь не удален
        try:
            db_user = user_queries.change_password(session, hashed_password, user_id)
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        # проверяем, что secret_word валидный и совпадает с тем, который находится в БД
        try:
            check_hash(request_model.secret_word, db_user.secret_word)
        except CheckPasswordHashException:
            raise SanicSecretWordHashException('Error')

        try:
            session.commit_session()
        except (DBIntegrityException, DBDataException) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(status=200)
