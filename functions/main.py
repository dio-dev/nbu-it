from utils import *


async def start(message: types.Message, state: FSMContext):


    await UserStates.start.set()

    reply_markup = InlineKeyboardMarkup(row_width=1)
    async with state.proxy() as data:
        btn1 = InlineKeyboardButton(text="Отделение банка", callback_data="type-1")
        btn2 = InlineKeyboardButton(text="Банкомат", callback_data="type-2")
        btn3 = InlineKeyboardButton(text="Обменник", callback_data="type-3")
        reply_markup.add(btn1, btn2, btn3)

        await bot.send_message(message.from_user.id,
                               "Я помогу найти ближайшие обьекты. \r\nЧто ты хочешь найти?", reply_markup=reply_markup)


async def show_bady_users(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    except Exception:
        print(sys.exc_info())

    await UserStates.showBody.set()

    reply_markup = InlineKeyboardMarkup(row_width=1)
    users = await get_buddy_candidates(callback_query.from_user.id)
    if shuffle_bady_list == "true":
        shuffle(users)
    counter = 0
    counter_photo = 0
    print(users)

    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_btn = KeyboardButton(text="↩ Назад")
    keyboard.add(back_btn)
    key_mess = await bot.send_message(callback_query.from_user.id, "..", reply_markup=keyboard)
    await bot.delete_message(callback_query.from_user.id, key_mess.message_id)

    async with state.proxy() as data:
        data["users"] = users
        data["userCounter"] = 0
        data["counter_photo"] = 0
        data["backFunction"] = "mainMenu"
        reply_markup.row_width = 2
        curr_user = users[0]
        data["badyUserId"] = curr_user.user_id
        user_name = curr_user.first_name
        finished_habits = curr_user.finished_habits
        pro_status = curr_user.pro_status
        print(curr_user.user_id)
        photo = await bot.get_user_profile_photos(curr_user.user_id)
        print(photo)
        prev = InlineKeyboardButton(text="◀", callback_data="prev")
        next = InlineKeyboardButton(text="▶", callback_data="next")
        change = InlineKeyboardButton(text="Предложить стать бади", callback_data="badyOffer")
        reply_markup.add(change)
        reply_markup.add(next)
        reply_markup_photo = InlineKeyboardMarkup(row_width=2)
        prev_photo = InlineKeyboardButton(text="◀", callback_data="prev_photo")
        next_photo = InlineKeyboardButton(text="▶", callback_data="next_photo")
        reply_markup_photo.add(prev_photo, next_photo)
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back_btn = KeyboardButton(text="↩ Назад")
        keyboard.add(back_btn)
        if pro_status == "vip":
            pro_status = "\r\nСтатус - 👑 VIP"
        else:
            pro_status = "Статус - Обычный"
        habits = await get_active_user_habits(curr_user.id)
        active_habits_text = "\r\nНет активных привычек\r\n"
        if len(habits) > 0:
            active_habits_text = "\r\nАктивные привычки:\r\n"
            counter_habit = 0
            for habit in habits:
                counter_habit += 1
                active_habits_text += str(counter_habit) + ". *" + habit[0] + "*\r\n"
        user_bady_count = await get_my_bady(curr_user.user_id)
        bady_count_text = "\r\nБез бади"
        if len(user_bady_count) > 0:
            bady_count_text = f"\r\nКол-во бади у пользователя - {str(len(user_bady_count))}"

        message_text = "Бади: \r\nИмя - {0}{1}{2}{3}".format(
            user_name, active_habits_text, pro_status, bady_count_text)

        await bot.send_message(callback_query.from_user.id,
                               "Выбери бади:", reply_markup=keyboard)
        print(len(photo["photos"]))
        if len(photo["photos"]) == 1:
            photos = photo["photos"][0]
            await bot.send_photo(callback_query.from_user.id, photo=photos[0]["file_id"],
                                 caption=message_text, reply_markup=reply_markup)
        elif len(photo["photos"]) > 1:
            photos = photo["photos"][data["counter_photo"]]
            photo_message = await bot.send_photo(callback_query.from_user.id, photo=photos[0]["file_id"],  reply_markup=reply_markup_photo)
            data["photo_message_id"] = photo_message.message_id
            await bot.send_message(callback_query.from_user.id, message_text, reply_markup=reply_markup)
        else:
            await bot.send_message(callback_query.from_user.id, message_text, reply_markup=reply_markup)


async def navigate_bady_photo(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        photo_counter = data["counter_photo"]
        users = await get_buddy_candidates(callback_query.from_user.id)
        counter = data["userCounter"]
        curr_user = users[counter]
        photo = await bot.get_user_profile_photos(curr_user.user_id)
        media = InputMedia()
        photo = photo["photos"]
        reply_markup_photo = InlineKeyboardMarkup(row_width=2)
        prev_photo = InlineKeyboardButton(text="◀", callback_data="prev_photo")
        next_photo = InlineKeyboardButton(text="▶", callback_data="next_photo")
        reply_markup_photo.add(prev_photo, next_photo)
        if callback_query.data == "prev_photo":
            if photo_counter != 0:
                photo_counter -= 1
            else:
                photo_counter = len(photo) - 1
        else:
            if photo_counter != len(photo) - 1:
                photo_counter += 1
            else:
                photo_counter = 0

        data['counter_photo'] = photo_counter
        media_photo = InputMediaPhoto(photo[photo_counter][0]["file_id"])
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=data["photo_message_id"],
                                     media=media_photo, reply_markup=reply_markup_photo)


async def remove_bady(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    except Exception:
        print(sys.exc_info())

    async with state.proxy() as data:
        bady_id = data["badyUserId"]
        bady_user = get_user_by_tg_id(bady_id)
        user = get_user_by_tg_id(callback_query.from_user.id)
        await remove_bady_db(user.id, bady_user.id)
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        back_btn = KeyboardButton(text="↩ Назад")
        keyboard.add(back_btn)
        mess = await bot.send_message(callback_query.from_user.id, f"Вы удалили бади {bady_user.first_name}",
                                      reply_markup=keyboard)


async def show_own_bady(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    except Exception:
        print(sys.exc_info())

    await UserStates.showOwnBody.set()

    reply_markup = InlineKeyboardMarkup(row_width=1)
    users = await get_my_bady(callback_query.from_user.id)
    counter = 0
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_btn = KeyboardButton(text="↩ Назад")
    keyboard.add(back_btn)
    key_mess = await bot.send_message(callback_query.from_user.id, "..", reply_markup=keyboard)
    await bot.delete_message(callback_query.from_user.id, key_mess.message_id)
    async with state.proxy() as data:

        if len(users) == 0:
            keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            back_btn = KeyboardButton(text="↩ Назад")
            keyboard.add(back_btn)
            prev = InlineKeyboardButton(text="Выбрать бади", callback_data="choiseBady")
            reply_markup.add(prev)
            mess = await bot.send_message(callback_query.from_user.id, "Проверка...", reply_markup=keyboard)
            await bot.delete_message(callback_query.from_user.id, mess.message_id)
            await bot.send_message(callback_query.from_user.id, "У Вас нету активных бади", reply_markup=reply_markup)
        elif len(users) > 0:

            data["users"] = users
            data["userCounter"] = 0
            data["backFunction"] = "mainMenu"
            reply_markup.row_width = 2
            curr_user = users[0]
            data["badyUserId"] = curr_user.user_id
            user_name = curr_user.first_name
            finished_habits = curr_user.finished_habits
            pro_status = curr_user.pro_status

            photo = await bot.get_user_profile_photos(curr_user.user_id)

            if len(photo["photos"]) > 0:
                photos = photo["photos"][0]
            prev = InlineKeyboardButton(text="◀", callback_data="prev")
            next = InlineKeyboardButton(text="▶", callback_data="next")
            change = InlineKeyboardButton(text="Удалить бади", callback_data="delete_bady")
            reply_markup.add(change)

            if len(users) > 1:
                reply_markup.add( next)

            keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            back_btn = KeyboardButton(text="↩ Назад")
            keyboard.add(back_btn)

            if pro_status == "vip":
                pro_status = "платная подписка"
            else:
                pro_status = "обычная подписка"
            message_text = "Бади: \r\nНикнейм - @{0}\r\nВыполненых привычек - {1}\r\nСтатус подписки - {2}".format(
                user_name, finished_habits, pro_status)

            await bot.send_message(callback_query.from_user.id,
                                   "Ваши бади:", reply_markup=keyboard)

            if len(photo["photos"]) > 0:
                photos = photo["photos"][0]
                await bot.send_photo(callback_query.from_user.id, photo=photos[0]["file_id"],
                                     caption=message_text, reply_markup=reply_markup)
            else:
                await bot.send_message(callback_query.from_user.id, message_text, reply_markup=reply_markup)


async def navigate_own_bady(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:

        if callback_query.data == "prev" or callback_query.data == "next":
            pass
        else:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    except Exception:
        print(sys.exc_info())

    await UserStates.showOwnBody.set()
    reply_markup = InlineKeyboardMarkup(row_width=1)

    async with state.proxy() as data:
        data["backFunction"] = "mainMenu"
        reply_markup.row_width = 2
        users = await get_my_bady(callback_query.from_user.id)
        if shuffle_bady_list == "true":
            shuffle(users)
        counter = data["userCounter"]
        if callback_query.data == "prev" and counter != 0:
            counter -= 1
        elif callback_query.data == "next" and counter < (len(users) - 1):
            counter += 1
        data["userCounter"] = counter
        curr_user = users[counter]
        data["badyUserId"] = curr_user.user_id
        user_name = curr_user.username
        finished_habits = curr_user.finished_habits
        pro_status = curr_user.pro_status
        prev = InlineKeyboardButton(text="◀", callback_data="prev")
        next = InlineKeyboardButton(text="▶", callback_data="next")
        change = InlineKeyboardButton(text="Удалить бади", callback_data="delete_bady")
        reply_markup.add(change)
        if counter >= (len(users)-1):
            reply_markup.add(prev)
        elif counter == 0:
            reply_markup.add(next)
        else:
            reply_markup.add(prev, next)
        photo = await bot.get_user_profile_photos(curr_user.user_id)
        if pro_status == "vip":
            pro_status = "платная подписка"
        else:
            pro_status = "обычная подписка"
        message_text = "Бади: \r\nНикнейм - @{0}\r\nВыполненых привычек - {1}\r\nСтатус подписки - {2}".format(
            user_name, finished_habits, pro_status)

        try:

            if len(photo["photos"]) > 0:
                photos = photo["photos"][0]
                await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                await bot.send_photo(callback_query.from_user.id, photo=photos[0]["file_id"],
                                     caption=message_text, reply_markup=reply_markup)

            else:
                await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                await bot.send_message(callback_query.from_user.id, message_text,
                                       reply_markup=reply_markup)
        except:
            print(sys.exc_info())


async def navigate_bady_users(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:

        if callback_query.data == "prev" or callback_query.data == "next":
            pass
        else:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    except Exception:
        print(sys.exc_info())

    await UserStates.showBody.set()
    reply_markup = InlineKeyboardMarkup(row_width=1)

    async with state.proxy() as data:
        data["backFunction"] = "mainMenu"
        data["counter_photo"] = 0
        reply_markup.row_width = 2
        users = await get_buddy_candidates(callback_query.from_user.id)
        if shuffle_bady_list == "true":
            shuffle(users)
        counter = data["userCounter"]
        if callback_query.data == "prev" and counter != 0:
            counter -= 1
        elif callback_query.data == "next" and counter < (len(users) - 1):
            counter += 1
        reply_markup_photo = InlineKeyboardMarkup(row_width=2)
        prev_photo = InlineKeyboardButton(text="◀", callback_data="prev_photo")
        next_photo = InlineKeyboardButton(text="▶", callback_data="next_photo")
        reply_markup_photo.add(prev_photo, next_photo)
        data["userCounter"] = counter
        curr_user = users[counter]
        data["badyUserId"] = curr_user.user_id
        first_name = curr_user.first_name
        user_name = ""
        last_name = curr_user.last_name
        if last_name is not None and first_name is not None and curr_user.username is not None:
            user_name = first_name + " " + last_name + f"({curr_user.username})"
        elif last_name is not None and first_name is not None and curr_user.username is None:
            user_name = first_name + " " + last_name
        elif last_name is not None and first_name is not None and curr_user.username is not None:
            user_name = last_name + f"({curr_user.username})"
        elif last_name is None and first_name is not None and curr_user.username is not None:
            user_name = first_name + f"({curr_user.username})"
        elif last_name is None and first_name is None and curr_user.username is not None:
            user_name = curr_user.username
        elif last_name is not None and first_name is None and curr_user.username is None:
            user_name = last_name
        elif last_name is None and first_name is not None and curr_user.username is None:
            user_name = first_name


        finished_habits = curr_user.finished_habits
        pro_status = curr_user.pro_status
        prev = InlineKeyboardButton(text="◀", callback_data="prev")
        next = InlineKeyboardButton(text="▶", callback_data="next")
        change = InlineKeyboardButton(text="Предложить стать бади", callback_data="badyOffer")
        reply_markup.add(change)
        print(counter)
        print(len(users))
        if counter >= (len(users)-1):
            reply_markup.add(prev)
        elif counter == 0:
            reply_markup.add(next)
        else:
            reply_markup.add(prev, next)
        photo = await bot.get_user_profile_photos(curr_user.user_id)
        if pro_status == "vip":
            pro_status = "\r\nСтатус - 👑 VIP"
        else:
            pro_status = "Статус - Обычный"
        habits = await get_active_user_habits(curr_user.id)
        active_habits_text = "\r\nНет активных привычек\r\n"
        if len(habits) > 0:
            active_habits_text = "\r\nАктивные привычки:\r\n"
            counter_habit = 0
            for habit in habits:
                counter_habit += 1
                active_habits_text += str(counter_habit) + ". *" + habit[0] + "*\r\n"
        user_bady_count = await get_my_bady(curr_user.user_id)
        bady_count_text = "\r\nБез бади"
        if len(user_bady_count) > 0:
            bady_count_text = f"\r\nКол-во бади у пользователя - {str(len(user_bady_count))}"

        message_text = "Бади: \r\nИмя - {0}{1}{2}{3}".format(
            user_name, active_habits_text, pro_status, bady_count_text)

        try:
            print(len(photo["photos"]))
            if len(photo["photos"]) == 1:
                photos = photo["photos"][0]
                try:
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.delete_message(callback_query.from_user.id, (int(callback_query.message.message_id - 1)))
                except:
                    pass
                await bot.send_photo(callback_query.from_user.id, photo=photos[0]["file_id"],
                                     caption=message_text, reply_markup=reply_markup, parse_mode="markdown")
            elif len(photo["photos"]) > 1:
                try:
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.delete_message(callback_query.from_user.id, (int(callback_query.message.message_id - 1)))
                except:
                    pass

                photos = photo["photos"][data["counter_photo"]]
                photo_message = await bot.send_photo(callback_query.from_user.id, photo=photos[0]["file_id"],
                                                     reply_markup=reply_markup_photo)
                data["photo_message_id"] = photo_message.message_id
                await bot.send_message(callback_query.from_user.id, message_text, reply_markup=reply_markup, parse_mode="markdown")
            else:
                try:
                    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
                    await bot.delete_message(callback_query.from_user.id, (int(callback_query.message.message_id - 1)))
                except:
                    pass
                await bot.send_message(callback_query.from_user.id, message_text,
                                       reply_markup=reply_markup, parse_mode="markdown")
        except:
            print(sys.exc_info())


async def remove_bady_confirm(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except Exception:
        print(sys.exc_info())

    await UserStates.removeBadyConfirm.set()

    async with state.proxy() as data:
        data["habbitAddType"] = "edit"
    reply_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = KeyboardButton(text="Да")
    btn2 = KeyboardButton(text="Нет")
    back_btn = KeyboardButton(text="📱 Главное меню")
    reply_markup.add(btn1, btn2, back_btn)

    await bot.send_message(callback_query.from_user.id,
                           f"Ты действительно хочешь *удалить* бади?", reply_markup=reply_markup, parse_mode="markdown")


async def send_bady_offer(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Start creating new Habbit
    """
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except Exception:
        print(sys.exc_info())
    await UserStates.badyMenu.set()

    async with state.proxy() as data:
        data["backFunction"] = "mainMenu"
        user = get_user_by_tg_id(callback_query.from_user.id)

        if user.pro_status != "vip":
            data["payment_source"] = "send_bady_offer"
            reply_markup = InlineKeyboardMarkup(row_width=1)
            keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            back_btn = KeyboardButton(text="↩ Назад")
            keyboard.add(back_btn)
            mess = await bot.send_message(callback_query.from_user.id,
                                          "В бесплатной версии бота Вы не можете добавлять бади",
                                          reply_markup=keyboard)
            # await bot.delete_message(message.from_user.id, mess.message_id)
            payload = str(callback_query.from_user.id) + str(datetime.datetime.now())
            prices = [
                types.LabeledPrice(label='Платая подписка', amount=24900),
            ]

            vip_btn = InlineKeyboardButton(text="💎 Открыть все возможности 💎", pay=True)
            reply_markup.add(vip_btn)
            await bot.send_invoice(callback_query.from_user.id, title='Платная подписка',
                                   description='Если тебе нужно больше бади, открой все возможности:\r\n😃 '
                                               'Неограниченные кол-во привычек\r\n👫 Неограниченное кол-во бади '
                                               'одновременно\r\n⏰ Сколько угодно напоминаний'
                                               'Все это всего за 249р в месяц. Оплати сейчас, чтобы не упустить скидку 😃',
                                   provider_token=PAYMENTS_PROVIDER_TOKEN,
                                   currency='RUB',
                                   prices=prices,
                                   start_parameter='subscribe',
                                   payload=payload,
                                   reply_markup=reply_markup)
        else:
            user_to_id = data["badyUserId"]

            request_id = add_bady_request(callback_query.from_user.id, user_to_id)

            keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            back_btn = KeyboardButton(text="📱 Главное меню")
            keyboard.add(back_btn)

            await bot.send_message(callback_query.from_user.id,
                                   "Запрос отправлен, я оповещу после решения пользователя", reply_markup=keyboard)

            message_text = "Пользователь {0} отправил запрос стать бади".format(callback_query.from_user.first_name)
            reply_markup = InlineKeyboardMarkup(row_width=1)
            accept = InlineKeyboardButton(text="👍 Принять",
                                          callback_data=f"acceptBadyRequest-{callback_query.from_user.id}-{request_id}")
            decide = InlineKeyboardButton(text="👎 Отклонить",
                                          callback_data=f"declineBadyRequest-{callback_query.from_user.id}-{request_id}")
            reply_markup.add(accept, decide)
            await bot.send_message(user_to_id,
                                   message_text, reply_markup=reply_markup)


async def accept_buddy_request(calback_query: types.CallbackQuery, state: FSMContext):
    # TODO: check if users are already baddies
    try:
        await bot.delete_message(calback_query.from_user.id, calback_query.message.message_id)
    except Exception:
        print(sys.exc_info())

    from_user_id = int(calback_query.data.split('-')[1])
    request_id = int(calback_query.data.split('-')[2])
    request = await get_request(request_id)
    user = get_user_by_tg_id(request.user_to_id)
    set_buddy_request_status(request_id, "accepted")
    reply_markup = InlineKeyboardMarkup()
    write_btn = InlineKeyboardButton(text="Написать бади", callback_data="show_buddy")
    reply_markup.add(write_btn)

    from_user = get_user_by_tg_id(from_user_id)
    user_to = get_user_by_tg_id(calback_query.from_user.id)
    messge_grac_text = f"Поздравляю, теперь ты с {user_to.first_name} бади. \r\nПривычки твоего нового бади:\r\n"
    habits = await get_active_user_habits(request.user_to_id)
    active_habits_text = "\r\nНет активных привычек\r\n"
    if len(habits) > 0:
        active_habits_text = ""
        counter_habit = 0
        for habit in habits:
            counter_habit += 1
            active_habits_text += str(counter_habit) + ". *" + habit[0] + "*\r\n"
    messge_grac_text += f"\r\nЕсли бади пропустит выполнение привычки, я обязательно сообщу тебе об этом.Поддерживай, или дай пинка, когда будет лениться 😁\r\nНаписать бади: @{user.username}"
    message_text = f" согласился стать вашим бади!"

    messge_grac_text_from = f"Поздравляю, теперь ты с {from_user.first_name} бади. \r\nПривычки твоего нового бади:\r\n"
    habits_from = await get_active_user_habits(request.user_from_id)
    active_habits_text = "\r\nНет активных привычек\r\n"
    if len(habits_from) > 0:
        active_habits_text = ""
        counter_habit = 0
        for habit in habits_from:
            counter_habit += 1
            active_habits_text += str(counter_habit) + ". *" + habit[0] + "*\r\n"
    messge_grac_text_from += f"\r\nЕсли бади пропустит выполнение привычки, я обязательно сообщу тебе об этом.Поддерживай, или дай пинка, когда будет лениться 😁\r\nНаписать бади: @{from_user.username}"
    message_text = f" согласился стать вашим бади!"
    await bot.send_message(from_user_id, messge_grac_text)
    await bot.send_message(request.user_to_id, messge_grac_text_from)
    add_baddies_pair(from_user.id, user_to.id)


async def show_buddy_nick(calback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        nick = data["buddy_nick"]

        await bot.send_message(calback_query.from_user.id, nick)


async def decline_buddy_request(calback_query: types.CallbackQuery):
    try:
        await bot.delete_message(calback_query.from_user.id, calback_query.message.message_id)
    except Exception:
        print(sys.exc_info())

    from_user_id = int(calback_query.data.split('-')[1])
    request_id = int(calback_query.data.split('-')[2])
    set_buddy_request_status(request_id, "declined")

    from_user = get_user_by_tg_id(from_user_id)
    user_to = get_user_by_tg_id(calback_query.from_user.id)
    message_text = f"{user_to.username} не захотел становиться вашим бадди!"
    #await bot.send_message(from_user_id, message_text)


async def send_kick_to_buddy(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except Exception:
        print(sys.exc_info())

    buddy_id = int(callback_query.data.split('-')[-1])
    buddy = get_user_by_id(buddy_id)
    from_user = get_user_by_tg_id(callback_query.from_user.id)

    await bot.send_message(chat_id=buddy.chat_id, text=f"{from_user.username} напоминает, что пора выполнить привычку")


async def send_link_to_buddy(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except Exception:
        print(sys.exc_info())

    buddy_id = int(callback_query.data.split('-')[-1])
    buddy = get_user_by_id(buddy_id)
    from_user = get_user_by_tg_id(callback_query.from_user.id)
    print(buddy.username)

    await bot.send_message(chat_id=from_user.chat_id, text=f"@{buddy.username}")