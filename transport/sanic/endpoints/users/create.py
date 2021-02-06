from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateUserDto
from api.response import ResponseGetUserDto

from db.database import DBSession
from db.queries import user as user_queries
from db.exceptions import DBIntegrityException, DBDataException, DBUserAlreadyExistsException

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicPasswordHashException, SanicDBException

from utils.password import generate_hash
from utils.password import GeneratePasswordHashException


# Endpoint для обработки запроса на создание пользователя
class CreateUserEndpoint(BaseEndpoint):

    async def method_post(
            self, request: Request, body: dict, session: DBSession, *args, **kwargs
    ) -> BaseHTTPResponse:

        # DTO объект
        request_model = RequestCreateUserDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
            secret_word = generate_hash(request_model.secret_word)
        except GeneratePasswordHashException as error:
            raise SanicPasswordHashException(str(error))

        try:
            # экземпляр базы данных
            db_user = user_queries.create_user(session, request_model, hashed_password, secret_word)
            session.commit_session()
        # ошибка уникальности, то есть подразумевается, что такой пользователь
        # уже существует в базе
        except DBUserAlreadyExistsException:
            return await self.make_response_json(status=409, message='User already exists')
        except (DBIntegrityException, DBDataException) as error:
            raise SanicDBException(str(error))

        response_model = ResponseGetUserDto(db_user)

        return await self.make_response_json(
            body=response_model.dump(),
            status=201
        )
