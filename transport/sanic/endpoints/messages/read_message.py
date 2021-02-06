from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseGetMessageDto

from db.database import DBSession
from db.exceptions import (
    DBUserDeletedException, DBIntegrityException, DBDataException, DBMessageNotFoundException,
    DBMessageDeletedException
)
from db.queries import user as user_queries
from db.queries import message as message_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import (
    SanicUserDeletedException, SanicDBException, SanicMessageNotFoundException, SanicMessageDeletedException
)


class ReadMessage(BaseEndpoint):
    async def method_get(
            self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            db_message = message_queries.get_message(session, msg_id, is_read=True)
        except DBMessageNotFoundException:
            raise SanicMessageNotFoundException('Message not found')
        except DBMessageDeletedException:
            raise SanicMessageDeletedException('Message deleted')

        # проверка на то, что пользователь читает сообщение от своего имени
        if token['id'] != db_message.recipient_id:
            return await self.make_response_json(status=403)

        # проверяем, что пользователь не удален
        try:
            user_queries.get_user(session=session, user_id=token['id'])
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        # коммитим изменения (статус is_read)
        try:
            session.commit_session()
        except (DBIntegrityException, DBDataException) as error:
            raise SanicDBException(str(error))

        response_model = ResponseGetMessageDto(db_message)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200
        )
