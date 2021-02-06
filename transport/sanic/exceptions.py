# обработка исключений, которые относятся конкретно к sanic'у (к транспортному уровню)

from sanic.exceptions import SanicException


# произошла ошибка валидации входных данных
class SanicRequestValidationException(SanicException):
    status_code = 400


# ситуация, когда user уже существует в БД
class SanicUserConflictException(SanicException):
    status_code = 409


# ошибка валидации ответных данных
class SanicResponseValidationException(SanicException):
    status_code = 500


# исключение, связанное с паролем
class SanicPasswordHashException(SanicException):
    status_code = 500


# исключение, связанное с секретным словом
class SanicSecretWordHashException(SanicException):
    status_code = 500


# исключение, связанное с БД
class SanicDBException(SanicException):
    status_code = 500


# user not found
class SanicUserNotFoundException(SanicException):
    status_code = 404


# пользователь удален
class SanicUserDeletedException(SanicException):
    status_code = 404


# не авторизированный пользователь
class SanicAuthException(SanicException):
    status_code = 401


class SanicMessageNotFoundException(SanicException):
    status_code = 404


class SanicMessageDeletedException(SanicException):
    status_code = 404
