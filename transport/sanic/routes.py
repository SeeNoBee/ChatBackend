# модуль для регистрации роутов

from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        # user
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=('GET', 'POST')
        ),
        endpoints.CreateUserEndpoint(
            config=config, context=context, uri='/user', methods=['POST']
        ),
        endpoints.AuthUserEndpoint(
            config=config, context=context, uri='/user/auth', methods=['POST']
        ),
        endpoints.GetUserEndpoint(
            config=config, context=context, uri='/user', methods=['GET'], auth_required=True,
        ),
        endpoints.GetUserByLoginEndpoint(
            config=config, context=context, uri='/user/get_user/<user_login:string>', methods=['GET'],
            auth_required=True
        ),
        endpoints.UserEndpoint(
            config=config, context=context, uri='/user/<user_id:int>', methods=['PATCH', 'DELETE'], auth_required=True
        ),
        endpoints.AllUsersEndpoint(
            config=config, context=context, uri='/user/all', methods=['GET'], auth_required=True
        ),
        endpoints.ChangePasswordEndpoint(
            config=config, context=context, uri='/user/change_password/<user_id:int>', methods=['PATCH'],
            auth_required=True,
        ),
        endpoints.ChangeLoginEndpoint(
            config=config, context=context, uri='/user/change_login/<user_id:int>', methods=['PATCH'],
            auth_required=True,
        ),
        endpoints.RestoreUserEndpoint(
            config=config, context=context, uri='user/restore/<login:string>', methods=['PATCH'],
            auth_required=True,
        ),

        # message
        endpoints.CreateMessage(
            config=config, context=context, uri='/message', methods=['POST'], auth_required=True,
        ),
        endpoints.GetAllMessagesEndpoint(
            config=config, context=context, uri='/message', methods=['GET'], auth_required=True,
        ),
        endpoints.MessageEndpoint(
            config=config, context=context, uri='/message/<msg_id:int>', methods=['PATCH', 'DELETE'], auth_required=True
        ),
        endpoints.ReadMessage(
            config=config, context=context, uri='/message/<msg_id:int>', methods=['GET'], auth_required=True
        ),
    )
