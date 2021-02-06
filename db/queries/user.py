# модуль для запросов касательно пользователя
import time
from typing import List

from api.request import RequestCreateUserDto, RequestPatchUserDto

from db.database import DBSession
from db.exceptions import DBUserAlreadyExistsException, DBUserNotFoundException, DBUserDeletedException
from db.models import DBUser

from context import Context, ContextLockedException


# создание модели пользователя в базе данных
def create_user(
        session: DBSession, user: RequestCreateUserDto, hashed_password: bytes, secret_word: bytes
) -> DBUser:
    # создание модели DBUser
    new_user = DBUser(
        login=user.login,
        password=hashed_password,  # записываем в базу хэшированный пароль
        first_name=user.first_name,
        last_name=user.last_name,
        secret_word=secret_word,
    )

    # сначала попробуем получить пользователя по login перед созданием записи в БД
    # если не None, то получается, что пользователь с таким логином уже есть в БД -> рейзим исключение
    if session.get_user_by_login(new_user.login) is not None:
        raise DBUserAlreadyExistsException

    # добавляем модель в базу данных
    session.add_model(new_user)

    return new_user


# получение пользователя
def get_user(session: DBSession, login: str = None, user_id: int = None, undelete: bool = False) -> DBUser:
    db_user = None

    if login is not None:
        db_user = session.get_user_by_login(login)
    elif user_id is not None:
        db_user = session.get_user_by_id(user_id)

    if db_user is None:
        raise DBUserNotFoundException

    if db_user.is_deleted is True:
        if not undelete:
            raise DBUserDeletedException

    return db_user


# изменение данных пользователя
def patch_user(
        session: DBSession, user: RequestPatchUserDto, user_id: int = None
) -> DBUser:

    db_user = None

    if user_id is not None:
        db_user = session.get_user_by_id(user_id)

    if db_user is None:
        raise DBUserNotFoundException

    if db_user.is_deleted is True:
        raise DBUserDeletedException

    # атрибуты, которые хотим изменить
    # attrs = ('first_name', 'last_name')
    # for attr in attrs:
    for attr in user.fields:
        if hasattr(user, attr):
            setattr(db_user, attr, getattr(user, attr))

    return db_user


def update_messages_stats(
        session: DBSession, *, user_id: int = None, login: str = None, role: str, context: Context
) -> DBUser:

    db_user = None

    if user_id is not None:
        db_user = session.get_user_by_id(user_id)
    elif login is not None:
        db_user = session.get_user_by_login(login)

    # to pretend data race
    while context.is_locked:
        time.sleep(0.05)

    context.lock()
    if role == 'sender':
        db_user.sent_messages += 1
    else:
        db_user.received_messages += 1
    context.unlock()

    return db_user


def change_password(session: DBSession, hashed_password: bytes, user_id: int) -> DBUser:

    db_user = session.get_user_by_id(user_id)

    if db_user.is_deleted:
        raise DBUserDeletedException

    db_user.password = hashed_password

    return db_user


def change_login(session: DBSession, new_login: str, user_id: int) -> DBUser:
    db_user_same_login = session.get_user_by_login(new_login)

    if db_user_same_login is not None:
        raise DBUserAlreadyExistsException

    db_user = session.get_user_by_id(user_id)

    if db_user.is_deleted:
        raise DBUserDeletedException

    # если исключение не зарейзилось, значит пользователь с таким логином отсутствует
    db_user.login = new_login

    return db_user


def delete_user(session: DBSession, user_id: int) -> DBUser:

    db_user = session.get_user_by_id(user_id)

    if db_user is None:
        raise DBUserNotFoundException

    if db_user.is_deleted is False:
        db_user.is_deleted = True
    else:
        raise DBUserDeletedException

    return db_user


def get_users(session: DBSession) -> List['DBUser']:
    return session.get_all_users()


def restore_user(login: str, session: DBSession):
    db_user = session.get_user_by_login(login)
    db_user.is_deleted = False

    return db_user
