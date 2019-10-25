from sqlalchemy import Column, String, Integer, Date, ForeignKey
from base import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', String(32))
    chat_id = Column('chat_id', String(32))
    first_name = Column('first_name', String(32))
    last_name = Column('last_name', String(32))
    username = Column('username', String(32))
    is_bot = Column('is_bot', String(32))
    language_code = Column('language_code', String(32))

    def __init__(self, user_id, chat_id, first_name, last_name, username, is_bot, language_code):
        self.user_id = user_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.finished_habits = 0
        self.is_bot = is_bot
        self.language_code = language_code
