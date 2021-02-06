import bcrypt

from utils.password.exceptions import GeneratePasswordHashException, CheckPasswordHashException


# генерируем hash пароля
def generate_hash(password_: str) -> bytes:
    try:
        # возвращаем хэшированный пароль и генерируем соль
        return bcrypt.hashpw(
            password=password_.encode(),  # аргумент password ожидает получить строку в виде байтов
            salt=bcrypt.gensalt(),
        )
    except (TypeError, ValueError) as error:
        raise GeneratePasswordHashException(str(error))


# проеряем hash пароля
def check_hash(password_: str, hash_: bytes) -> None:
    try:
        # проверяем совпадает ли хэш пароля с тем, который у нас в базе
        result = bcrypt.checkpw(
            password=password_.encode(),
            hashed_password=hash_,
        )
    except (TypeError, ValueError) as error:
        raise CheckPasswordHashException(str(error))

    if not result:
        raise CheckPasswordHashException
