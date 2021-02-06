from sqlalchemy import Column, String, Boolean, LargeBinary, Integer

from db.models import BaseModel


class DBUser(BaseModel):

    # название для таблица - как она будет называться в базе данных
    __tablename__ = 'users'

    login = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    password = Column(
        LargeBinary(),
        nullable=False
    )

    first_name = Column(String(50))
    last_name = Column(String(50))

    secret_word = Column(
        LargeBinary(),
        nullable=False
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    sent_messages = Column(
        Integer,
        default=0,
    )

    received_messages = Column(
        Integer,
        default=0,
    )
