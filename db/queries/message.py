from typing import List

from api.request import RequestCreateMessageDto, RequestPatchMessageDto

from db.database import DBSession
from db.exceptions import DBMessageNotFoundException, DBMessageDeletedException
from db.models import DBMessage


def create_message(
        session: DBSession, message: RequestCreateMessageDto, token: dict, recipient_id: int
) -> DBMessage:
    # создание модели DBMessage
    new_message = DBMessage(
        message=message.message,
        sender_id=token['id'],
        recipient_id=recipient_id,
    )

    # добавляем модель в БД
    session.add_model(new_message)

    return new_message


def get_message(session: DBSession, msg_id: int = None, is_read: bool = None) -> DBMessage:
    db_message = None

    if msg_id is not None:
        db_message = session.get_message_by_id(msg_id)

    if db_message is None:
        raise DBMessageNotFoundException

    if db_message.is_deleted is True:
        raise DBMessageDeletedException

    if is_read:
        db_message.is_read = True

    return db_message


def get_all_messages(session: DBSession, user_id: int) -> List['DBMessage']:
    messages = session.get_all_messages(user_id)
    list_of_messages = [message for message in messages if message.is_deleted is not True]

    return list_of_messages


def patch_message(session: DBSession, message: RequestPatchMessageDto, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)

    attr = 'message'
    if hasattr(message, attr):
        setattr(db_message, attr, getattr(message, attr))

    return db_message


def delete_message(session: DBSession, msg_id: int) -> DBMessage:
    db_message = session.get_message_by_id(msg_id)

    db_message.is_deleted = True

    return db_message
