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
    habits_count = Column('habits_count', Integer)
    pro_status = Column('pro_status', String(32))
    finished_habits = Column('finished_habits_count', Integer)
    dateStart = Column('date_start', Date())
    exit_status = Column('exit_status', String(32))
    exit_date = Column('exit_date', Date())
    start_message_id = Column('start_message_id', String())

    def __init__(self, user_id, chat_id, first_name, last_name, username, is_bot, language_code, date_start, start_message_id):
        self.user_id = user_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.finished_habits = 0
        self.is_bot = is_bot
        self.language_code = language_code
        self.habits_count = 0
        self.exit_status = "false"
        self.dateStart = date_start
        self.start_message_id = start_message_id
        self.pro_status = "standart"
