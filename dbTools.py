from itertools import product
from datetime import date
import datetime
import sys
from sqlalchemy import or_, and_
from base import Session, engine, Base
from models.Users import Users
from models.Habits import Habits
from models.HabitsEvents import HabitsEvents
from models.StandartHabits import StandartHabits
from models.HabitsSchedule import HabitsSchedule
from models.Reviews import Reviews
from models.BadyRequest import BadyRequest
from models.Buddies import Buddies
from models.Payment import Payment
from models.HabitsBlackNote import HabitsBlackNote

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


def db_create_habit(user_id, name, reminder_days, reminder_time, min_req, start_time):
    session.commit()
    user = session.query(Users) \
        .filter(Users.user_id == user_id) \
        .first()

    date_now = datetime.date.today()
    habit = Habits(user, name, date_now, min_req, start_time)
    session.add(habit)
    session.commit()

    for weekday, daytime in product(reminder_days, reminder_time):
        habit_schedule = HabitsSchedule(habit, user.id, weekday, daytime)
        session.add(habit_schedule)

        session.commit()


async def get_habit_events(habit_id):
    session.commit()
    events = session.query(HabitsEvents) \
        .filter(HabitsEvents.habit_id == habit_id) \
        .all()

    session.commit()

    return events

async def db_create_habit_black_note(user_id, name):
    session.commit()
    user = session.query(Users) \
        .filter(Users.user_id == user_id) \
        .first()

    date_now = datetime.datetime.today()
    habit = HabitsBlackNote(user, name, date_now)
    session.add(habit)
    session.commit()
    return habit.id


async def db_update_habit_black_note(habit_id, info_type, info_value):

    session.commit()
    update = {}
    date_now = datetime.datetime.today()
    if info_type == "week_days":
        update = {HabitsBlackNote.week_days: info_value, HabitsBlackNote.date_create: date_now, HabitsBlackNote.step: "time"}
    elif info_type == "time":
        update = {HabitsBlackNote.time: info_value, HabitsBlackNote.date_create: date_now, HabitsBlackNote.step: "start_time"}
    elif info_type == "finished_status":
        update = {HabitsBlackNote.finished_status: info_value, HabitsBlackNote.date_create: date_now}
    elif info_type == "send_status":
        update = {HabitsBlackNote.send_status: info_value, HabitsBlackNote.date_create: date_now}


    session.query(HabitsBlackNote).filter(HabitsBlackNote.id == habit_id).update(update, synchronize_session=False)
    session.commit()


async def check_habit_black_note():

    habits_black_note = session.query(HabitsBlackNote).filter(and_(HabitsBlackNote.finished_status != "true", HabitsBlackNote.send_status != "true")).all()
    return habits_black_note


async def get_habit_black_note(user_id):

    habits_black_note = session.query(HabitsBlackNote)\
        .filter(and_(HabitsBlackNote.finished_status != "true", HabitsBlackNote.user_id == user_id)).first()
    return habits_black_note


def db_edit_habit(user_id, habit_id, reminder_days, reminder_time, min_req, start_time, name):
    session.commit()

    user = session.query(Users).filter(Users.user_id == user_id).first()
    habit = session.query(Habits).filter(Habits.id == habit_id).first()
    session.query(HabitsSchedule).filter(HabitsSchedule.habit_id == habit_id) \
        .update({HabitsSchedule.finished_status: "unactive"}, synchronize_session=False)
    session.query(Habits).filter(Habits.id == habit_id) \
        .update({Habits.start_time: start_time, Habits.name: name}, synchronize_session=False)

    for weekday, daytime in product(reminder_days, reminder_time):
        habit_schedule = HabitsSchedule(habit, user.id, weekday, daytime)
        session.add(habit_schedule)

        session.commit()


async def remove_habit_db(habit_id):
    session.commit()

    habit = session.query(Habits).filter(Habits.id == habit_id) \
        .update({Habits.finished_status: "true"}, synchronize_session=False)
    session.query(HabitsSchedule).filter(HabitsSchedule.habit_id == habit_id) \
        .update({HabitsSchedule.finished_status: "unactive"}, synchronize_session=False)

    session.commit()


def get_habits_schedule():
    session.commit()
    return session.query(HabitsSchedule).filter(HabitsSchedule.finished_status == "active").all()


def get_user_buddies(user_id):
    session.commit()
    buddies = session.query(Buddies.user_to_id).filter(Buddies.user_from_id == user_id).all() + \
        session.query(Buddies.user_from_id).filter(Buddies.user_to_id == user_id).all()
    buddies = [item[0] for item in buddies]
    return session.query(Users).filter(Users.id.in_(buddies)).all()


def get_habits_schedule_in_range(weekday, time, time_range):
    session.commit()
    start_range = (time - time_range).time()
    end_range = time.time()
    return session.query(HabitsSchedule).filter(
        and_(
            HabitsSchedule.finished_status == 'active',
            HabitsSchedule.reminder_weekday == weekday,
            HabitsSchedule.reminder_time >= start_range,
            HabitsSchedule.reminder_time <= end_range
        )
    ).all()


def get_events_by_habit(habit: Habits, from_time):
    return session.query(HabitsEvents).filter(
        and_(HabitsEvents.date >= from_time,
             HabitsEvents.habit_id == habit.id)
    ).all()


def get_habits_count(user_id):
    habits = []

    try:
        user = session.query(Users) \
            .filter(Users.user_id == user_id) \
            .first()
        habits = session.query(Habits) \
            .filter(and_(Habits.user_id == user.id, Habits.finished_status != "true")) \
            .all()
        session.commit()

    except:
        session.rollback()

    return len(habits)


def get_habits(user_id):
    habits = []
    session.commit()

    try:
        user = session.query(Users) \
            .filter(Users.user_id == user_id) \
            .first()
        print(user.id)
        habits = session.query(Habits) \
            .filter(and_(Habits.user_id == user.id,
                         Habits.finished_status != "true")) \
            .all()
        session.commit()

    except:
        session.rollback()

    return habits


async def get_habit_by_id(id):
    return session.query(Habits).filter(Habits.id == id).first()


def check_habit_event(habit_id, user_id):
    habit_object = {}
    date_now = datetime.date.today()

    try:
        habit = session.query(HabitsEvents) \
            .filter(HabitsEvents.habit_id == habit_id) \
            .filter(HabitsEvents.user_id == user_id) \
            .filter(HabitsEvents.date == date_now) \
            .all()
        habit_object = habit
        session.commit()

    except:
        session.rollback()
        habit = session.query(HabitsEvents) \
            .filter(HabitsEvents.habit_id == habit_id) \
            .filter(HabitsEvents.user_id == user_id) \
            .filter(HabitsEvents.date == date_now) \
            .all()
        habit_object = habit
        session.commit()

    return habit_object


def add_habit_event(habit_id, user_id, event_type, mood=None, note=None, file_id=None, file_type=None):
    habit_object = {}
    habit = session.query(Habits) \
        .filter(Habits.id == habit_id) \
        .all()
    habit_object = habit[0]
    session.commit()

    date_now = datetime.datetime.today()

    try:
        habit_ev = session.query(HabitsEvents) \
            .filter(HabitsEvents.habit_id == habit_id) \
            .filter(HabitsEvents.user_id == user_id) \
            .filter(HabitsEvents.date == date_now) \
            .all()

        if len(habit_ev) > 0:
            habit_object_ev = habit_ev[0]
            session.delete(habit_object_ev)

        session.commit()

    except:
        habit_ev = session.query(HabitsEvents) \
            .filter(HabitsEvents.habit_id == habit_id) \
            .filter(HabitsEvents.user_id == user_id) \
            .filter(HabitsEvents.date == date_now) \
            .all()

        if len(habit_ev) > 0:
            habit_object_ev = habit_ev[0]
            session.delete(habit_object_ev)
        session.commit()

    event = HabitsEvents(habit_object, user_id, event_type, date_now, mood, note, file_id, file_type)
    session.merge(event)
    session.commit()
    return event


async def get_event_by_id(event_id):
    session.commit()
    event = session.query(HabitsEvents).filter(HabitsEvents.id == event_id).first()
    return event


async def increase_day_counter(habit_id):
    session.commit()
    day_counter = session.query(Habits.days_counter).filter(Habits.id == habit_id).first()[0]
    day_counter += 1
    upd_review = session.query(Habits).filter(Habits.id == habit_id). \
        update({Habits.days_counter: day_counter}, synchronize_session=False)
    session.commit()
    return day_counter


async def finish_habit(habit_id, user_id):
    session.commit()
    session.query(Habits).filter(Habits.id == habit_id). \
        update({Habits.finished_status: "true"}, synchronize_session=False)

    session.query(HabitsSchedule).filter(HabitsSchedule.habit_id == habit_id). \
        update({HabitsSchedule.finished_status: "true"}, synchronize_session=False)

    habit_counter = session.query(Users.finished_habits).filter(Users.user_id == user_id).first()
    habit_counter += 1
    session.query(Users).filter(Users.user_id == user_id). \
        update({Users.finished_habits: habit_counter}, synchronize_session=False)
    session.commit()


async def renew_habit(habit_id):
    session.commit()
    session.query(Habits).filter(Habits.id == habit_id). \
        update({Habits.finished_status: "false", Habits.days_counter: 0}, synchronize_session=False)

    session.query(HabitsSchedule).filter(HabitsSchedule.habit_id == habit_id). \
        update({HabitsSchedule.work_status: "active"}, synchronize_session=False)
    session.commit()


def get_standart_habits():
    habits = []

    try:
        habits = session.query(StandartHabits) \
            .all()
        session.commit()

    except:
        session.rollback()
        habits = session.query(StandartHabits) \
            .all()
        session.commit()

    return habits


def get_date(dateStr):
    date_args = dateStr.split(".")
    year = int(date_args[2])
    month = int(date_args[1])
    day = int(date_args[0])

    return date(year, month, day)


def get_standart_habit(id):
    habits = []

    try:
        habits = session.query(StandartHabits) \
            .filter(StandartHabits.id == id) \
            .all()
        session.commit()

    except:
        session.rollback()
        habits = session.query(StandartHabits) \
            .filter(StandartHabits.id == id) \
            .all()
        session.commit()

    return habits


def add_review(user_id, review_text):
    try:
        user = session.query(Users) \
            .filter(Users.user_id == user_id) \
            .all()

        review = Reviews(user[0], review_text, datetime.date.today())
        session.add(review)
        session.commit()

    except:
        session.rollback()
        user = session.query(Users) \
            .filter(Users.user_id == user_id) \
            .all()

        review = Reviews(user[0], review_text, datetime.date.today())
        session.add(review)
        session.commit()


def get_analytic_data(habit_id):
    try:
        answer = {}
        events_execute = session.query(HabitsEvents) \
            .filter(and_(HabitsEvents.habit_id == habit_id, HabitsEvents.event_type == "execute")) \
            .all()
        events_failed = session.query(HabitsEvents) \
            .filter(and_(HabitsEvents.habit_id == habit_id, HabitsEvents.event_type == "failed")) \
            .all()

        habit = session.query(Habits) \
            .filter(Habits.id == habit_id) \
            .first()
        answer.update(
            {"name": habit.name, "day_remain": (14 - habit.days_counter), "execute_count": len(events_execute),
             "failed_count": len(events_failed)})
        session.commit()

        return answer

    except:
        session.rollback()


async def get_buddy_candidates(user_tg_id):
    session.commit()
    user = session.query(Users).filter(Users.user_id == user_tg_id).first()
    bady_list_from = session.query(Buddies.user_to_id).filter(
        and_(Buddies.user_from_id == user.id, Buddies.status == "active")).all()
    bady_list_to = session.query(Buddies.user_from_id).filter(
        and_(Buddies.user_to_id == user.id, Buddies.status == "active")).all()
    finish_arr = []
    if bady_list_from and bady_list_to:
        for item in bady_list_from:
            finish_arr.append(item[0])
        for item in bady_list_to:
            finish_arr.append(item[0])

    elif bady_list_to:
        for item in bady_list_to:
            finish_arr.append(item[0])
    else:
        for item in bady_list_from:
            finish_arr.append(item[0])
    users = session.query(Users).filter(and_(Users.user_id != user_tg_id, Users.id.notin_(finish_arr))).all()
    session.commit()

    return users


async def get_my_bady(user_tg_id):
    session.commit()
    user = session.query(Users).filter(Users.user_id == user_tg_id).first()
    bady_list_from = session.query(Buddies.user_to_id).filter(
        and_(Buddies.user_from_id == user.id, Buddies.status == "active")).all()
    bady_list_to = session.query(Buddies.user_from_id).filter(
        and_(Buddies.user_to_id == user.id, Buddies.status == "active")).all()
    finish_arr = []
    if bady_list_from and bady_list_to:
        for item in bady_list_from:
            finish_arr.append(item[0])
        for item in bady_list_to:
            finish_arr.append(item[0])

    elif bady_list_to:
        for item in bady_list_to:
            finish_arr.append(item[0])
    else:
        for item in bady_list_from:
            finish_arr.append(item[0])
    users = session.query(Users).filter(and_(Users.user_id != user_tg_id, Users.id.in_(finish_arr))).all()
    session.commit()

    return users


async def get_request(request_id):
    session.commit()
    request = session.query(BadyRequest). \
        filter(BadyRequest.id == request_id). \
        first()
    session.commit()
    return request


async def remove_bady_db(user_id, bady_id):
    session.commit()
    session.query(Buddies). \
        filter(or_(and_(Buddies.user_to_id == user_id, Buddies.user_from_id == bady_id),
                   and_(Buddies.user_to_id == bady_id, Buddies.user_from_id == user_id))). \
        update({Buddies.status: "deleted"}, synchronize_session=False)
    session.commit()


def add_bady_request(user_id, user_to_id):
    session.commit()
    bady_request = BadyRequest(user_id, user_to_id, "send", datetime.date.today())
    session.add(bady_request)
    session.commit()
    return bady_request.id


def set_buddy_request_status(request_id, status: str):
    session.commit()
    request = session.query(BadyRequest).filter(BadyRequest.id == request_id).first()
    request.request_status = status
    session.commit()


def get_user_by_id(user_id):
    session.commit()
    return session.query(Users).filter(Users.id == user_id).first()


def get_user_by_tg_id(tg_id):
    session.commit()
    return session.query(Users).filter(Users.user_id == tg_id).first()


async def get_reviews():
    session.commit()
    return session.query(Reviews).all()


async def get_review_by_id(review_id):
    session.commit()
    return session.query(Reviews).filter(Reviews.id == review_id).first()


async def update_review(review_id, answer_text):
    session.commit()

    upd_review = session.query(Reviews).filter(Reviews.id == review_id). \
        update({Reviews.answer_status: "true", Reviews.answer_text: answer_text}, synchronize_session=False)

    session.commit()


def add_baddies_pair(user_id1, user_id2):
    baddies_pair = Buddies(
        user_from_id=user_id1,
        user_to_id=user_id2,
        date_create=datetime.datetime.now(),
        status="active"
    )

    session.add(baddies_pair)
    session.commit()


async def add_payment(user_id, payload, provider_payment_charge_id, telegram_payment_charge_id, amount, currency):
    user = session.query(Users).filter(Users.id == user_id).first()
    payment = Payment(user, payload, provider_payment_charge_id, telegram_payment_charge_id, amount, currency,
                      datetime.date.today())

    session.add(payment)
    session.commit()


async def change_user_pro_status(user_id, status):
    session.commit()
    session.query(Users).filter(Users.id == user_id). \
        update({Users.pro_status: status}, synchronize_session=False)
    session.commit()


async def get_active_users():
    return session.query(Users).filter(Users.exit_status != "true").all()


async def get_active_user_habits(user_id):
    return session.query(Habits.name).filter(and_(Habits.finished_status != "true", Habits.user_id == user_id)).all()