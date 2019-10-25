from itertools import product
from datetime import date
import datetime
import sys
from sqlalchemy import or_, and_
from base import Session, engine, Base
from models.Users import Users

session = Session()


def add_user(user_id, chat_id, first_name, last_name, username, is_bot, language_code, start_message_id):
    try:
        session.commit()
        user = session.query(Users) \
            .filter(Users.user_id == user_id) \
            .all()

        if len(user) == 0:
            user = Users(user_id, chat_id, first_name, last_name, username, is_bot, language_code,
                         datetime.date.today(), start_message_id)
            session.add(user)
            session.commit()
            return 1
        else:
            return 0

    except:
        session.rollback()
        print(sys.exc_info())

