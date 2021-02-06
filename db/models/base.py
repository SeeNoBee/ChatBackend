# модуль для базового класса моделей

import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP


# получаем базовый класс, который обозначает таблицу в базе данных
Base = declarative_base()


class BaseModel(Base):

    # необходимо для того, чтобы эта таблица не создавалась просто так, а создавалась тогда,
    # когда наследуется
    __abstract__ = True

    # id элемента в таблице
    id = Column(
        Integer,
        nullable=False,  # не пустое
        unique=True,
        primary_key=True,
        autoincrement=True,  # предусмотрено автоувеличение
    )

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,  # при обновлении автоматически меняет значение
    )

    def __repr__(self):
        return f'{self.__class__.__name__}'
