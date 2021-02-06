from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMessageDto
from api.response import ResponseGetMessageDto

from db.database import DBSession
from db.exceptions import (
    DBIntegrityException, DBDataException, DBUserDeletedException, DBMessageNotFoundException,
    DBMessageDeletedException
)
from db.queries import user as user_queries
from db.queries import message as message_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import (
    SanicDBException, SanicUserDeletedException, SanicMessageDeletedException, SanicMessageNotFoundException
)


class MessageEndpoint(BaseEndpoint):

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        # проверяем, что сообщение есть в БД и не удалено
        try:
            db_message = message_queries.get_message(session, msg_id)
        except DBMessageNotFoundException:
            raise SanicMessageNotFoundException('Message not found')
        except DBMessageDeletedException:
            raise SanicMessageDeletedException('Message deleted')

        # проверка на то, что пользователь редактирует сообщение, отправленное от его имени
        if token['id'] != db_message.sender_id:
            return await self.make_response_json(status=403)

        # проверяем, что пользователь не удален
        try:
            user_queries.get_user(session=session, user_id=token['id'])
        except DBUserDeletedException:
            raise SanicUserDeletedException('User deleted')

        request_model = RequestPatchMessageDto(body)

        message = message_queries.patch_message(session, request_model, msg_id)

        try:
            session.commit_session()
        except (DBIntegrityException, DBDataException) as error:
            raise SanicDBException(str(error))

        response_model = ResponseGetMessageDto(message)

        return await self.make_response_json(
            body=response_model.dump(),
            status=200
        )

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        # проверяем, что сообщение есть в БД и не удалено
        try:
            db_message = message_queries.get_message(session, msg_id)
        except DBMessageNotFoundException:
            raise SanicMessageNotFoundException('Message not found')
        except DBMessageDeletedException:
            raise SanicMessageDeletedException('Message deleted')

        # проверка на то, что пользователь пытается удалить сообщение, которое ему отправили
        if token['id'] != db_message.recipient_id:
            return await self.make_response_json(status=403)

        message_queries.delete_message(session, msg_id)

        try:
            session.commit_session()
        except (DBIntegrityException, DBDataException) as error:
            raise SanicDBException(str(error))

        return await self.make_response_json(status=204)
