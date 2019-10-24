import asyncio
import datetime

from aiogram.types.inline_keyboard import *
from aiogram.types.reply_keyboard import *
from dbTools import get_habits_schedule, db_update_habit_black_note, check_habit_black_note, get_habits_schedule_in_range, get_events_by_habit, get_user_buddies, get_user_by_id, add_habit_event, check_habit_event
from utils import bot

weekdays = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')


async def send_reminder():
    habits_schedule = get_habits_schedule()
    now = datetime.datetime.now()

    for habit_schedule in habits_schedule:
        if habit_schedule.habit.start_time == 'tomorow':
            #print(habit_schedule.habit.start_time)
            if habit_schedule.habit.date_create == now.date():
                continue

        try:
            if now.weekday() == habit_schedule.reminder_weekday and \
                    (now - datetime.timedelta(seconds=60)).time() < habit_schedule.reminder_time < now.time():
                inline_kb1 = InlineKeyboardMarkup()
                btn11 = InlineKeyboardButton("✅ Выполнить", callback_data=f'success-{habit_schedule.habit.id}')
                btn12 = InlineKeyboardButton("❌ Пропустить", callback_data=f'failed-{habit_schedule.habit.id}')
                inline_kb1.add(btn11, btn12)
                await bot.send_message(chat_id=habit_schedule.user.chat_id, text=f"Пора выполнить привычку: \r\n{habit_schedule.habit.name}",
                                       reply_markup=inline_kb1)
            if now.weekday() == habit_schedule.reminder_weekday and \
                    (datetime.time(23, 55, 0)) < now.time() < datetime.time(0, 0, 0):
                habit_event = check_habit_event(habit_schedule.habit_id, habit_schedule.user.chat_id)
                if len(habit_event) == 0:
                    add_habit_event(habit_schedule.habit_id, habit_schedule.user.chat_id, "failed")
        except Exception as e:
            print(str(e))


async def check_buddy_skip():
    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds=1800)

    habits_schedule = get_habits_schedule_in_range(now.date().weekday(),
                                                   now,
                                                   delta)
    print(habits_schedule)
    for habit_schedule in habits_schedule:
        habit_events = get_events_by_habit(habit_schedule.habit, now - delta)
        user = get_user_by_id(habit_schedule.user_id)
        if len(habit_events) == 0:
            buddies = get_user_buddies(habit_schedule.user_id)
            for buddy in buddies:
                inline_kb1 = InlineKeyboardMarkup()
                btn11 = InlineKeyboardButton("Дать пинка", callback_data=f'kick-{user.id}')
                btn12 = InlineKeyboardButton("Написать бади", callback_data=f'write-{user.id}')
                inline_kb1.add(btn11, btn12)
                try:
                    await bot.send_message(buddy.chat_id, text=f"{user.username} *ленится* выполнить привычку",
                                       reply_markup=inline_kb1, parse_mode="Markdown")
                except:
                    pass


async def check_habit_unfinish():
    now_time = datetime.datetime.now()
    delta = datetime.timedelta(seconds=600)
    black_notes = await check_habit_black_note()
    for black_note in black_notes:
        date_update = black_note.date_create
        if (now_time - delta).time() > date_update.time():
            user = get_user_by_id(black_note.user_id)
            reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn = KeyboardButton(text="Перейти к созданию привычки")
            back_btn = KeyboardButton(text="📱 Главное меню")
            reply_markup.add(btn, back_btn)
            await bot.send_message(user.user_id, "Мы с тобой не завершили создание привычки\r\nДавай сделаем это 😃",
                                   reply_markup=reply_markup)
            await db_update_habit_black_note(black_note.id, "send_status", "true")




async def start_checker():
    counter = 0
    while True:
        await send_reminder()
        await check_habit_unfinish()
        if counter % (3600 / 60) == 0:
            await check_buddy_skip()

        counter += 1
        await asyncio.sleep(60)

