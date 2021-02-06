from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.user.restore_user import RequestRestoreUserDto

from db.database import DBSession
from db.exceptions import DBUserNotFoundException, DBDataException, DBIntegrityException
from db.queries import user as user_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicDBException


class RestoreUserEndpoint(BaseEndpoint):

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, login: str, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            db_user = user_queries.get_user(session=session, login=login, undelete=True)
        except DBUserNotFoundException:
            raise SanicUserNotFoundException('User not found')

        if token['id'] != db_user.id:
            return await self.make_response_json(status=403)

        request_model = RequestRestoreUserDto(body)

        user_queries.restore_user(request_model.login, session)

        try:
            session.commit_session()
        except (DBIntegrityException, DBDataException) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(status=200)
