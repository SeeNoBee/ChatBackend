# файл для настройки конфигов всего приложения


from transport.sanic.config import SanicConfig
from db.config import SQLiteConfig, PostgresConfig


class ApplicationConfig:
    sanic: SanicConfig
    # database: SQLiteConfig
    database: PostgresConfig

    def __init__(self):
        self.sanic = SanicConfig()
        # self.database = SQLiteConfig()
        self.database = PostgresConfig()
