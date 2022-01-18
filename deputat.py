import datetime
import random
import res
from telebot import types


def get_deputat(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT userid, deputatid FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    db_object.execute("SELECT deputatid FROM deputats WHERE deputatid IS NOT NULL ORDER BY deputatid DESC LIMIT 1")
    last_deputat = db_object.fetchone()
    if result is None:
        if last_deputat is None:
            deputat_id = -2147483648
        else:
            deputat_id = last_deputat[0] + 1
        db_object.execute(
            "INSERT INTO deputats(userid, money, name, level, photo, username, deputatid, rating) VALUES "
            "( %s, %s, %s, %s, %s, %s, %s, %s)",
            (user_id, random.randint(10, 100), random.choice(res.deputatNames), 1,
             random.randint(0, len(res.level_photos[0]) - 1),
             message.from_user.first_name, deputat_id, 0))
        db_connection.commit()
        bot.reply_to(message, "Осьо! Ваш перший дєпутат! Позирити на нього - /show")
    elif result[1] is None:
        if last_deputat is None:
            deputat_id = -2147483648
        else:
            deputat_id = last_deputat[0] + 1
        db_object.execute("UPDATE deputats SET deputatid = %s, money = %s, name = %s, level = %s,  photo = %s, "
                          "rating = %s WHERE userid = %s", (deputat_id, random.randint(10, 100), random.choice(
                           res.deputatNames), 1, random.randint(0, len(res.level_photos[0]) - 1), 0, result[0]))
        db_connection.commit()
        bot.reply_to(message, "Гля який! Депута-а-а-атіще! Глянуть на підарасіка - /show")
    else:
        bot.reply_to(message, "В тебе вже є депутат")
        bot.send_sticker(message.chat.id, res.what_sticker)


def show_deputat(message, db_object, bot):
    user_id = message.from_user.id
    db_object.execute(
        f"SELECT name, money, level, photo, deputatid, rating FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result or result[4] is None:
        bot.reply_to(message, "Ніхуя нема...")
    else:
        reply_message = ""
        deputat_photo = res.level_photos[result[2] - 1][result[3]]
        reply_message += f"👨🏻 Ім'я: {result[0]}\n💰 Бабло: ${result[1]}\n⭐️ Рейтинг: {result[5]}" \
                         f"\n📚 Рівень: {result[2]} - {res.level_captions[result[2] - 1]} "
        bot.send_photo(message.chat.id, deputat_photo, reply_to_message_id=message.id, caption=reply_message)


def _work_(data, user_id, db_object, db_connection):
    today_str = datetime.datetime.today().strftime("%Y-%m-%d")
    earned = random.randint(10, 100) * res.money_earn_multiplier[data[1] - 1]
    db_object.execute("UPDATE deputats SET lastworked = %s, money = %s WHERE userid = %s",
                      (today_str, earned + int(data[0]), user_id))
    db_connection.commit()
    return earned


def work_deputat(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT lastworked FROM deputats WHERE deputats.userid = {user_id}")
    last_worked = db_object.fetchone()
    db_object.execute(f"SELECT money, level, name, deputatid FROM deputats WHERE deputats.userid = {user_id}")
    data = db_object.fetchone()
    if not last_worked or data[3] is None:
        bot.reply_to(message, "В тебе нема депутата, шоб він працював")
    elif not last_worked[0]:
        earned = _work_(data, user_id, db_object, db_connection)
        bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                       caption=f"{data[2]}{res.work_text[data[1] - 1]}\n💰 Дохід: ${earned}",
                       reply_to_message_id=message.id)
    else:
        worked = last_worked[0]
        today = datetime.date.today()
        if (today - worked).days >= 1:
            earned = _work_(data, user_id, db_object, db_connection)
            bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                           caption=f"{data[2]}{res.work_text[data[1] - 1]}\n💰 Дохід: ${earned}")
        else:
            bot.send_photo(message.chat.id, random.choice(res.not_working_photos),
                           caption="Твій депутат вже заїбався бо нині відхуячив своє", reply_to_message_id=message.id)


def lvlup_deputat(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT level, money, deputatid FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result or result[2] is None:
        bot.reply_to(message, "А шо апати то?")
    elif result[0] == res.MAX_LEVEL:
        bot.reply_to(message, "В депутата максимальний рівень!")
    elif result[1] < res.lvlup_requirements[result[0] - 1]:
        bot.reply_to(message, f"Твій депутат надто бідний, щоб перейти на новий рівень!"
                              f"\n💰 Необхідно грошей: ${res.lvlup_requirements[result[0] - 1]}")
        bot.send_sticker(message.chat.id, res.sad_sticker)
    else:
        db_object.execute("UPDATE deputats SET level = %s, photo = %s, lastworked = NULL, money = %s WHERE userid = %s",
                          (result[0] + 1, random.randint(0, len(res.level_photos[result[0]]) - 1),
                           result[1] - res.lvlup_requirements[result[0] - 1], user_id))
        db_connection.commit()
        bot.reply_to(message, "Депутата підвищено до нового рівня! - /show")
        bot.send_sticker(message.chat.id, res.happy_sticker)


def _create_buttons_(modifier, message, db_object, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT kid, negr, kiosk FROM business WHERE userid = {user_id}")
    result = db_object.fetchone()
    if result is None:
        bot.reply_to(message, "Бізнесів не знайдено!")
        bot.send_sticker(message.chat.id, res.sad_sticker)
        return
    buttons = types.InlineKeyboardMarkup()
    for i in range(len(res.biz_prices)):
        if result[i] is not None:
            buttons.add(types.InlineKeyboardButton(text=res.biz_provide_buttons(result, i), callback_data=f'{modifier}{i}'))
    bot.reply_to(message, res.biz_text, reply_markup=buttons)


def visit_business_deputat(message, db_object, bot):
    _create_buttons_('vb', message, db_object, bot)


def handle_visit_business_deputat(call, db_object, db_connection, bot):
    user_id = call.from_user.id
    biz_id = int(call.data[2:3])
    biz_name = res.biz_db_name[biz_id]
    biz_work = biz_name + 'work'
    biz_visit = biz_name + 'visit'
    db_object.execute(f"SELECT deputatid, {biz_name}, {biz_visit}, {biz_work} FROM business WHERE userid = {user_id}")
    result = db_object.fetchone()
    db_object.execute(f"SELECT money FROM deputats WHERE userid = {user_id}")
    money = db_object.fetchone()
    deputat_id = result[0]
    biz_count = result[1]
    visited = result[2] if result[2] is not None else datetime.date.min
    worked = result[3] if result[3] is not None else datetime.date.min
    today = datetime.date.today()
    if not result or deputat_id is None or biz_count is None:
        bot.send_message(call.message.chat.id, "І кого ти провідуєш? Мать свою чи шо?")
    elif (today - worked).days < 1:
        bot.send_message(call.message.chat.id, res.biz_worked_text[biz_id])
    elif (today - visited).days >= 7:
        bot.send_message(call.message.chat.id, res.biz_not_visited_text[biz_id])
    else:
        earned = res.biz_profits[biz_id] * random.randint(1, 10)
        db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s",
                          (money[0] + earned, user_id))
        db_connection.commit()
        today_str = datetime.datetime.today().strftime("%Y/%m/%d")
        db_object.execute(f"UPDATE business SET {biz_work} = %s WHERE userid=%s", (today_str, user_id))
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_photos[biz_id], caption=res.biz_work_text[biz_id] + str(earned))


def provide_business_deputat(message, db_object, bot):
    _create_buttons_('pb', message, db_object, bot)


def handle_provide_business_deputat(call, db_object, db_connection, bot):
    user_id = call.from_user.id
    biz_id = int(call.data[2:3])
    biz_name = res.biz_db_name[biz_id]
    biz_visit = biz_name + 'visit'
    db_object.execute(f"SELECT deputatid, {biz_name}, {biz_visit} FROM business WHERE userid = {user_id}")
    result = db_object.fetchone()
    db_object.execute(f"SELECT money FROM deputats WHERE userid = {user_id}")
    money = db_object.fetchone()
    deputat_id = result[0]
    biz_count = result[1]
    visited = result[2] if result[2] is not None else datetime.date.min
    today = datetime.date.today()
    days_diff = (today - visited).days
    if not result or deputat_id is None or biz_count is None:
        bot.send_message(call.message.chat.id, "І кого ти провідуєш? Мать свою чи шо?")
    elif visited is not None and days_diff < 7:
        bot.send_message(call.message.chat.id, f"Бізнес не потребує забезпечення, приходьте за {7-days_diff} днів")
    elif money[0] < res.biz_provides[biz_id] * biz_count:
        bot.send_message(call.message.chat.id, "В твого депутата замало грошей для підтримання цього бізнесу!")
        bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
    else:
        db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s", (money[0] - res.biz_provides[biz_id] * biz_count, user_id))
        db_connection.commit()
        today_str = datetime.datetime.today().strftime("%Y/%m/%d")
        db_object.execute(f"UPDATE business SET {biz_visit} = %s WHERE userid=%s", (today_str, user_id))
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_provide_photos[biz_id], caption=res.biz_provide_text[biz_id])


def buy_business_deputat(message, bot):
    buttons = types.InlineKeyboardMarkup()
    for i in range(len(res.biz_prices)):
        buttons.add(types.InlineKeyboardButton(text=res.biz_name[i] + f"💰{res.biz_prices[i]}", callback_data=f'bb{i}'))
    buttons.add(types.InlineKeyboardButton(text="І шо мені вибирати?", callback_data="help"))
    bot.reply_to(message, res.biz_text, reply_markup=buttons)


def purchase_update(db_connection, db_object, bot, call, result, biz_id, user_id):
    db_connection.commit()
    db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s",
                      (result[1] - res.biz_prices[biz_id], user_id))
    db_connection.commit()
    bot.send_photo(call.message.chat.id, res.biz_photos[biz_id],
                   caption=f"Ви успішно купили \"{res.biz_name[biz_id]}\"!")


def handle_biz_purchase_deputat(call, db_object, db_connection, bot):
    user_id = call.from_user.id
    db_object.execute(f"SELECT deputatid, money FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    if not result or result[0] is None:
        bot.send_message(call.message.chat.id, "І кому ти зібрався купляти? Собі чи шо?")
        return
    biz_id = int(call.data[2:3])
    if result[1] < res.biz_prices[biz_id]:
        bot.send_message(call.message.chat.id, "Твій депутат надто бідний, шоб купити о це вот")
        bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
        return
    db_object.execute(f"SELECT kid, negr, kiosk, deputatid FROM business WHERE userid = {user_id}")
    deputat_id = db_object.fetchone()
    if deputat_id is None:
        db_object.execute(f"INSERT INTO business(userid, deputatid, {res.biz_db_name[biz_id]})"
                          f" VALUES(%s, %s, 1)", (user_id, result[0]))
        purchase_update(db_connection, db_object, bot, call, result, biz_id, user_id)
    else:
        if deputat_id[biz_id] is None:
            biz = 1
        else:
            biz = deputat_id[biz_id] + 1
        db_object.execute(f"UPDATE business SET {res.biz_db_name[biz_id]} = %s WHERE userid = %s",
                          (biz, user_id))
        db_connection.commit()
        purchase_update(db_connection, db_object, bot, call, result, biz_id, user_id)


def show_business_deputat(message, db_object, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT kid, negr, kiosk FROM business WHERE userid = {user_id}")
    result = db_object.fetchone()
    if not result:
        bot.reply_to(message, "У тебе нема депутата, або бізнесів!")
    else:
        reply_text = "Бізнеси твого депутата:"
        for i in range(len(result)):
            if result[i] is not None:
                reply_text += f"\n{res.biz_name[i]} - {result[i]}"
        bot.reply_to(message, reply_text)
        bot.send_sticker(message.chat.id, res.money_pagulich_sticker)


def kill_deputat(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT deputatid, killed FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    if not result:
        bot.reply_to(message, "А шо вбивати то?")
    elif result[0] is None:
        bot.reply_to(message, "Себе грохнути хочеш, чи шо?")
    else:
        if result[1] is None:
            killed = 0
        else:
            killed = result[1]
        db_object.execute(
            "UPDATE deputats SET deputatid = NULL, lastworked = NULL, killed = %s WHERE userid = %s",
            ((killed + 1), user_id))
        db_connection.commit()
        db_object.execute("DELETE FROM business WHERE userid = %s", [user_id])
        db_connection.commit()
        bot.reply_to(message, "Депутату розірвало сраку...\nОтримати нового - /get")


def killed_deputats(message, db_object, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT killed FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    if result is None or result[0] is None:
        bot.reply_to(message, "Ти ще не вбивав своїх депутатів")
    else:
        bot.reply_to(message, f"Вбито депутатів: {result[0]}")
