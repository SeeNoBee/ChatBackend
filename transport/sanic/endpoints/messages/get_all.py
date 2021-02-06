from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseGetMessageDto

from db.database import DBSession
from db.exceptions import DBUserNotFoundException, DBUserDeletedException
from db.queries import message as message_queries
from db.queries import user as user_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicUserDeletedException


class GetAllMessagesEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            user_queries.get_user(session, user_id=token['id'])
        except DBUserNotFoundException:
            raise SanicUserNotFoundException('User not found')
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        db_message = message_queries.get_all_messages(session, token['id'])

        response_model = ResponseGetMessageDto(db_message, many=True)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200,
        )
