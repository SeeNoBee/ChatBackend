# основной класс для обработки исключений паролей
class PasswordHashException(Exception):
    pass


class GeneratePasswordHashException(PasswordHashException):
    pass


class CheckPasswordHashException(PasswordHashException):
    pass
