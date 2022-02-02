import res
import random
import datetime
from telebot import types


# sets minimal possible id
def _set_deputat_id(deputat, last_deputat):
    db_object = deputat.db_object
    deputat_id = -9223372036854775808       # set minimal value for type int in PostgreSQL
    if last_deputat is not None:    # user is not first in DB
        while True:                 # run through all users and check if there is a deputat with that ID
            sql_deputat_id = f"SELECT user_id FROM deputats WHERE deputat_id = {deputat_id}"
            db_object.execute(sql_deputat_id)
            dep = db_object.fetchone()
            if dep is None:         # if deputat was not found
                break               # id is suitable, we will use it
            else:                   # else, we will try a bigger one
                deputat_id += 1
    return deputat_id


# commits to DB work-info, returns earned money
def _work_(deputat, user_id, money, level):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
    earned = random.randint(10, 100) * res.money_earn_multiplier[level - 1]
    db_object.execute("UPDATE deputats SET last_worked = %s, money = %s WHERE user_id = %s",
                      (today_str, earned + int(money), user_id))
    db_connection.commit()
    return earned


# gives user a deputat
def get_deputat(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    user_name = call.from_user.username
    user_firstname = call.from_user.first_name
    chat_id = call.message.chat.id

    sql_user_info = f"SELECT user_id, deputat_id FROM users WHERE user_id = {user_id}"
    db_object.execute(sql_user_info)
    user = db_object.fetchone()

    sql_deputat_info = f"SELECT deputat_id FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_deputat_info)
    deput = db_object.fetchone()

    sql_last_deputat = f"SELECT deputat_id FROM deputats ORDER BY deputat_id DESC"
    db_object.execute(sql_last_deputat)
    last_deputat = db_object.fetchone()

    if user is None and deput is None:  # user is not registered, use INSERT
        deputat_id = _set_deputat_id(deputat, last_deputat)
        sql_new_user = f"INSERT INTO users(user_id, user_name, user_firstname, deputat_id, killed_deputats) VALUES(" \
                       f"{user_id}, {user_name}, {user_firstname}, {deputat_id}, {0})"
        db_object.execute(sql_new_user)
        db_connection.commit()

        sql_new_deputat = f"INSERT INTO deputats(deputat_id, user_id, deputat_name, money, rating, level, photo)" \
                          f" VALUES( {deputat_id}, {user_id}, {random.choice(res.deputatNames)}," \
                          f" {random.randint(10, 100)}, {0}, {1}," \
                          f" {random.randint(0, len(res.level_photos[0]) - 1)}"
        db_object.execute(sql_new_deputat)
        db_connection.commit()
        bot.send_message(chat_id, "Осьо! Ваш перший дєпутат! Позирити на нього - /show")

    elif user is not None and deput is None:     # user doesn't have a deputat, use UPDATE
        deputat_id = _set_deputat_id(deputat, last_deputat)
        sql_new_deputat = f"INSERT INTO deputats(deputat_id, user_id, deputat_name, money, rating, level, photo)" \
                          f" VALUES( {deputat_id}, {user_id}, {random.choice(res.deputatNames)}," \
                          f" {random.randint(10, 100)}, {0}, {1}," \
                          f" {random.randint(0, len(res.level_photos[0]) - 1)}"
        db_object.execute(sql_new_deputat)
        db_connection.commit()
        bot.send_message(chat_id, "Гля який! Депута-а-а-атіще! Глянуть на підарасіка - /show")
    else:
        bot.answer_callback_query(call.id, "Ти чо, в тебе вже є депутат", show_alert=True)


# show info about user's deputat
def show_deputat(deputat, call):
    db_object = deputat.db_object
    bot = deputat.bot
    user_id = call.from_user.id
    sql_get_deputat = f"SELECT deputat_id, deputat_name, money, rating, level, photo FROM deputats " \
                      f"WHERE user_id = {user_id}"
    db_object.execute(sql_get_deputat)
    deput = db_object.fetchone()

    if deput is None:   # if user is not in DB or user doesn't have a deputat
        bot.answer_callback_query(call.id, "А де а хто а шо", show_alert=True)
    else:               # user has deputat, show info
        deputat_photo = res.level_photos[deput[4] - 1][deput[5]]
        reply_message = f"👨🏻 Ім'я: {deput[1]}\n💰 Бабло: ${deput[2]}\n⭐️ Рейтинг: {deput[3]}" \
                        f"\n📚 Рівень: {deput[4]} - {res.level_captions[deput[4] - 1]} "
        bot.send_photo(call.message.chat.id, deputat_photo, caption=reply_message)


# makes user's deputat work
def work_deputat(deputat, call):
    db_object = deputat.db_object
    bot = deputat.bot
    user_id = call.from_user.id

    sql_last_worked = f"SELECT last_worked, money, level, deputat_name FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_last_worked)
    deput = db_object.fetchone()

    last_worked = deput[0]
    money = deput[1]
    level = deput[2]
    deputat_name = deput[3]

    if deput is None:
        bot.answer_callback_query(call.id, "В тебе нема депутата, шоб він працював", show_alert=True)
    elif deput[0] is None:            # if works first time ever
        earned = _work_(deputat, user_id, money, level)
        bot.send_photo(call.message.chat.id, res.work_photos[level - 1],
                       caption=f"{deputat_name}{res.work_text[level - 1]}\n💰 Дохід: ${earned}")
    else:                               # if worked earlier
        worked = datetime.date(last_worked.year, last_worked.month, last_worked.day) - datetime.timedelta(hours=res.hour_adjust)
        today = datetime.date.today()
        if (today - worked).days >= 1:  # didn't work in a day
            earned = _work_(deputat, user_id, money, level)
            bot.send_photo(call.message.chat.id, res.work_photos[level - 1],
                           caption=f"{deputat_name}{res.work_text[level - 1]}\n💰 Дохід: ${earned}")
        else:                           # if worked today
            bot.send_photo(call.message.chat.id, random.choice(res.not_working_photos),
                           caption="Твій депутат вже заїбався бо нині відхуячив своє")


# upgrade user's rating
def up_rating_deputat(deputat, call):
    bot = deputat.bot
    chat_id = call.message.chat.id
    buttons = types.InlineKeyboardMarkup()
    for i in range(len(res.rating_name)):
        buttons.add(types.InlineKeyboardButton
                    (text=res.rating_name[i] + ' $' + str(res.rating_price[i]), callback_data=f'rt{i}'))
    buttons.add((types.InlineKeyboardButton(text="Назад", callback_data="deputat_menu")))
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=buttons)
    bot.edit_message_text("Доступні методи підняття рейтингу", call.message.chat.id, call.message.message_id)


# rating upgrade handler
def handle_rating_deputat(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    rating = int(call.data[2:3])

    sql_get_user_info = f"SELECT money, rating FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_get_user_info)
    deput = db_object.fetchone()

    if deput is None:     # if user doesn't have a deputat
        bot.answer_callback_query(call.id, "Дурак чи шо, кому ти туво купляєш")
    elif deput[0] < res.rating_price[rating]:  # if user doesn't have enough money
        bot.send_message(call.message.chat.id, "Твоєму депутату не вистачає грошей для цього!")
        bot.send_sticker(call.message.chat.id, res.sad_sticker)
    else:                                       # upgrade rating
        sql_update_rating = f"UPDATE deputats SET rating = {deput[1] + res.rating_up[rating]} " \
                            f"WHERE user_id = {user_id}"
        db_object.execute(sql_update_rating)
        db_connection.commit()
        sql_update_money = f"UPDATE deputats SET money = {deput[0] - res.rating_price[rating]} " \
                           f"WHERE user_id = {user_id}"
        db_object.execute(sql_update_money)
        db_connection.commit()
        bot.send_message(call.message.chat.id, f"Рейтинг серед громади піднято на {res.rating_up[rating]}⭐️")


# level-ups deputat
def lvlup_deputat(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    sql_get_user_info = f"SELECT level, money, rating FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_get_user_info)
    result = db_object.fetchone()

    if result is None:     # deputat was not found
        bot.answer_callback_query(call.id, "Кого ти блять апаєш, може депутата перше дістанеш?", show_alert=True)
    elif result[0] >= 4:   # level too high to lvlup
        bot.answer_callback_query(call.id, "Смарі, ти вже дохуя піздатий, тому шоб бути піздатішим треба на вибори "
                                           "податись окда", show_alert=True)
    elif result[1] < res.lvlup_requirements[result[0] - 1] or result[2] < res.lvlup_rating[result[0] - 1]:  # $ or rtng
        bot.send_message(chat_id, f"Твій депутат надто бідний, або має замалий рейтинг, щоб перейти на "
                                  f"новий рівень!\n💰 Необхідно грошей: "
                                  f"${res.lvlup_requirements[result[0] - 1]}\n⭐ Необхідно рейтингу: "
                                  f"{res.lvlup_rating[result[0] - 1]}")
        bot.send_sticker(chat_id, res.sad_sticker)
    else:                                   # deputat will lvlup
        sql_lvlup = f"UPDATE deputats SET level = {result[0] + 1}," \
                    f" photo = {random.randint(0, len(res.level_photos[result[0]]) - 1)}," \
                    f" last_worked = NULL, money = {result[1] - res.lvlup_requirements[result[0] - 1]}" \
                    f" WHERE user_id = {user_id}"
        db_object.execute(sql_lvlup)
        db_connection.commit()
        bot.send_message(chat_id, "Депутата підвищено до нового рівня! - /show")
        bot.send_sticker(chat_id, res.happy_sticker)


# back to deputat menu
def handle_deputat_menu(deputat, call):
    bot = deputat.bot
    buttons = types.InlineKeyboardMarkup()
    get = types.InlineKeyboardButton(text='Получити дєпутата', callback_data="get_deputat")
    show = types.InlineKeyboardButton(text='Позирити на депутата', callback_data="show_deputat")
    work = types.InlineKeyboardButton(text='Працювати', callback_data="work_deputat")
    rating = types.InlineKeyboardButton(text='Підвищити рейтинг', callback_data="rating_deputat")
    lvlup = types.InlineKeyboardButton(text='Підвищити рівень', callback_data="lvlup_deputat")
    buttons.add(get, show, work, rating, lvlup)
    bot.edit_message_reply_markup(call.message.chat_id, call.message.message_id, reply_markup=buttons)
    bot.edit_message_text(res.biz_text, call.message.chat.id, call.message.message_id)
