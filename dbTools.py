import sys
from base import Session
from models.Users import Users
from models.NbuObjects import NbuObject
from models.Location import Location

session = Session()


def add_user(user_id, chat_id, first_name, last_name, username, is_bot, language_code, start_message_id):
    try:
        session.commit()
        user = session.query(Users) \
            .filter(Users.user_id == user_id) \
            .all()

        if len(user) == 0:
            user = Users(user_id, chat_id, first_name, last_name, username, is_bot, language_code)
            session.add(user)
            session.commit()
            return 1
        else:
            return 0

    except:
        session.rollback()
        print(sys.exc_info())


def get_nbu_objects():
    session.commit()
    objects = session.query(NbuObject).all()
    session.commit()

    return objects


def create_location(region, city, street, building_number, adress_index):
    session.commit()
    location = Location(region, city, street, building_number, adress_index)
    session.add(location)
    session.commit()

    return location


def update_location(location_id, region, city, street, building_number, adress_index):
    session.commit()
    session.query(Location).filter(Location.id == location_id). \
        update({Location.region: region, Location.city: city, Location.street: street,
                Location.building_number: building_number, Location.adress_index: adress_index},
               synchronize_session=False)
    session.commit()
