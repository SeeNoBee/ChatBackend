from sqlalchemy import Column, String, Integer, Boolean

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    message = Column(
        String(100),
    )

    sender_id = Column(
        Integer,
        nullable=False
    )

    recipient_id = Column(
        Integer,
        nullable=False
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False,
    )
