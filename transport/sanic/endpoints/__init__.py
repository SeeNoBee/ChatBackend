from .base import BaseEndpoint
from .users.create import CreateUserEndpoint
from .users.auth import AuthUserEndpoint
from .users.get_user_by_login import GetUserByLoginEndpoint
from .users.user import UserEndpoint
from .users.user_info import GetUserEndpoint
from .users.get_all import AllUsersEndpoint
from .users.user_password import ChangePasswordEndpoint
from .users.user_login import ChangeLoginEndpoint
from .users.restore_user import RestoreUserEndpoint
from .health import HealthEndpoint

from .messages.create import CreateMessage
from .messages.get_all import GetAllMessagesEndpoint
from .messages.message import MessageEndpoint
from .messages.read_message import ReadMessage
