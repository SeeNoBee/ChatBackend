# вспомогательный модуль для создания и чтения токенов

import datetime

import jwt
from jwt.exceptions import PyJWTError

from utils.auth.config import UtilsConfig
from utils.auth.exceptions import ReadTokenException


# функция для генерации токена
def create_token(data: dict, lifetime: int = 1) -> str:
    # ключ будет действителен 1 час
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=lifetime)
    }
    payload.update(data)
    return jwt.encode(payload, UtilsConfig.secret_token, algorithm='HS256')


# на выходе получаем словарь с payload
def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, UtilsConfig.secret_token, algorithms='HS256')
    except PyJWTError:
        raise ReadTokenException
