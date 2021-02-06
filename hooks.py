# модуль, который должен быть выполнен при старте программы
# в данном случае получается подключение к базе данных

from sqlalchemy import create_engine

from context import Context
from configs.config import ApplicationConfig
from db.database import DataBase


def init_db_sqlite(config: ApplicationConfig, context: Context):
    # создаем вызов нашей базы данных
    engine = create_engine(
        config.database.url,
        pool_pre_ping=True,  # для переподключения
    )

    database = DataBase(connection=engine)
    database.check_connection()

    context.set('database', database)

