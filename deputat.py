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
    today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
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
        today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
        if (today - worked).days >= 1:
            earned = _work_(data, user_id, db_object, db_connection)
            bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                           caption=f"{data[2]}{res.work_text[data[1] - 1]}\n💰 Дохід: ${earned}")
        else:
            bot.send_photo(message.chat.id, random.choice(res.not_working_photos),
                           caption="Твій депутат вже заїбався бо нині відхуячив своє", reply_to_message_id=message.id)


def lvlup_deputat(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT level, money, deputatid, rating FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result or result[2] is None:
        bot.reply_to(message, "А шо апати то?")
    elif result[0] == 4:
        bot.reply_to(message, "Для підвищення рівня, необхідно ініціювати вибори!")
    elif result[1] < res.lvlup_requirements[result[0] - 1]:
        bot.reply_to(message, f"Твій депутат надто бідний, щоб перейти на новий рівень!"
                              f"\n💰 Необхідно грошей: ${res.lvlup_requirements[result[0] - 1]}")
        bot.send_sticker(message.chat.id, res.sad_sticker)
    elif result[3] < res.lvlup_rating[result[0] - 1]:
        bot.reply_to(message, f"У твого депутата надто низький рейтинг, щоб перейти на новий рівень!"
                              f"\n⭐ Необхідно рейтингу: {res.lvlup_rating[result[0] - 1]}")
        bot.send_sticker(message.chat.id, res.sad_sticker)
    else:
        db_object.execute("UPDATE deputats SET level = %s, photo = %s, lastworked = NULL, money = %s WHERE userid = %s",
                          (result[0] + 1, random.randint(0, len(res.level_photos[result[0]]) - 1),
                           result[1] - res.lvlup_requirements[result[0] - 1], user_id))
        db_connection.commit()
        bot.reply_to(message, "Депутата підвищено до нового рівня! - /show")
        bot.send_sticker(message.chat.id, res.happy_sticker)


def elections_deputat(message, db_object, bot):
    if message.chat.type == "private":
        bot.reply_to(message, "І шо блять? Ти тут один, тому сю команду в груповий чат писать надо да")
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton(text="Подати свою кандидатуру", callback_data='ela'))
    buttons.add(types.InlineKeyboardButton(text="Забрати свою кандидатуру", callback_data='eld'))
    buttons.add(types.InlineKeyboardButton(text="Завершити набір кандидатів", callback_data='els'))
    chat_id = message.chat.id
    db_object.execute(
        f"SELECT username, name FROM deputats JOIN elections e on deputats.userid = e.userid WHERE chatid = CAST({chat_id} AS varchar)")
    result = db_object.fetchall()
    names = ""
    for resul in result:
        names += f"\n{resul[1]} ({resul[0]})"
    bot.reply_to(message, f"Ініційовано початок виборів! Кандидати:{names}", reply_markup=buttons)


def start_election(message, db_object, bot, chat_id):
    db_object.execute(f"SELECT username, name, photo, level, money, rating, e.votes FROM deputats "
                      f"JOIN elections e on deputats.userid = e.userid WHERE chatid = CAST({chat_id} AS varchar) order by e.userid")
    result = db_object.fetchall()
    if result is None:
        bot.send_message(message.chat.id, "Каво, куда і шо...")
    else:
        i = 1
        bot.send_message(message.chat.id, "ВО ТОВО ВАШІ КАНДИДАТИ Є")
        for ress in result:
            text = str(i) + ' ' + ress[1] + ' (' + ress[0] + ') 💰' + str(ress[4]) + '$ ⭐' + str(ress[5]) + ' 📊' + str(ress[6])
            bot.send_photo(message.chat.id, res.level_photos[ress[3]-1][ress[2]], caption=text)
            i += 1
        bot.send_message(message.chat.id, "Для голосування введіть команду /vote та номер кандидата відповідно до вище наданого списку\nНаприклад: /vote 3 - проголосувати за 3 кандидата")


def _show_candidates_(call, db_object, db_connection, bot, chat_id):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton(text="Подати свою кандидатуру", callback_data='ela'))
    buttons.add(types.InlineKeyboardButton(text="Забрати свою кандидатуру", callback_data='eld'))
    buttons.add(types.InlineKeyboardButton(text="Завершити набір кандидатів", callback_data='els'))

    db_object.execute(f"SELECT username, name FROM deputats "
                      f"JOIN elections e on deputats.userid = e.userid WHERE chatid = CAST({chat_id} AS varchar)")
    result = db_object.fetchall()
    names = ""
    for resul in result:
        names += f"\n{resul[1]} ({resul[0]})"
    bot.edit_message_text(f"Ініційовано початок виборів! Кандидати:{names}", call.message.chat.id,
                          call.message.message_id, reply_markup=buttons)


def handle_elect_deputat(call, db_object, db_connection, bot):
    user_id = call.from_user.id
    chat_id = str(call.message.chat.id)
    call_type = call.data[2:3]
    if call_type == 's':
        isadmin = False
        admins_t = bot.get_chat_administrators(call.message.chat.id)
        for admin in admins_t:
            if user_id == admin.user.id:
                isadmin = True
                break
        if not isadmin:
            bot.send_message(call.message.chat.id, "Ти хто такий шоб сюда тикать, сука? АДМІНА ЗОВИ!!!")
            return
        db_object.execute(f"SELECT COUNT(*) FROM elections WHERE chatid = CAST({chat_id} AS varchar)")
        count = db_object.fetchone()
        if count is None or count[0] < 3:
            bot.send_message(call.message.chat.id, "Замало кандидатів! Мінімум 3 чибзоїда")
        else:
            bot.send_message(call.message.chat.id, "Вибори почались!")
            start_election(call.message, db_object, bot, call.message.chat.id)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        return
    if call_type == 'd':
        db_object.execute(f"SELECT userid FROM elections WHERE userid = {user_id}")
        result = db_object.fetchone()
        if result is None:
            return
        db_object.execute(f"DELETE FROM elections WHERE userid = {user_id}")
        db_connection.commit()
        _show_candidates_(call, db_object, db_connection, bot, chat_id)
        bot.send_message(call.message.chat.id, "Вашу кандідатуру видалено!")
        return

    db_object.execute(f"SELECT level, name, username FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    db_object.execute(f"SELECT level FROM deputats JOIN elections e on deputats.userid = e.userid")
    level = db_object.fetchone()
    if result is None or result[0] is None:
        bot.send_message(call.message.chat.id, "У вас нема депутата!")
    elif result[0] < 4:
        bot.send_message(call.message.chat.id, "У вас замалий рівень для подання кандидатури!")
    elif level is not None and result[0] != level[0]:
        bot.send_message(call.message.chat.id, "У вас опше не той рівень шо у кандидатів!")
    elif result[0] == res.MAX_LEVEL:
        bot.send_message(call.message.chat.id, "У вашого депутата максимальний рівень!")
    else:
        db_object.execute(f"SELECT userid FROM elections WHERE userid = {user_id}")
        result = db_object.fetchone()
        if result is not None:
            bot.send_message(call.message.chat.id, "Ваша кандидатура вже на виборах!")
        else:
            db_object.execute(f"INSERT INTO elections(userid, chatid, votes) VALUES({user_id}, {chat_id}, 0)")
            db_connection.commit()
            _show_candidates_(call, db_object, db_connection, bot, chat_id)


def election_vote(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    db_object.execute(f"SELECT COUNT(*) FROM elections WHERE chatid = CAST({chat_id} AS varchar)")
    count = db_object.fetchone()
    db_object.execute(f"SELECT userid FROM voted WHERE chatid = CAST({chat_id} AS varchar) and userid = {user_id}")
    result = db_object.fetchone()
    vote = int(message.text[6:])
    if count is None or vote <= 0 or vote > count[0] or result is not None:
        bot.send_message(message.chat.id, "Уїбати чи в'єбати?")
        return
    vote -= 1
    db_object.execute(f"SELECT votes FROM elections WHERE chatid = CAST({chat_id} AS varchar) order by userid OFFSET {vote} LIMIT 1")
    result = db_object.fetchone()
    votes = int(result[0]) + 1
    db_object.execute(f"UPDATE elections SET votes = {votes} WHERE chatid = CAST({chat_id} AS varchar) and userid = (select userid from elections order by userid offset {vote} limit 1)")
    db_connection.commit()
    db_object.execute(f"INSERT INTO voted(userid, chatid) VALUES {user_id, chat_id}")
    db_connection.commit()
    bot.send_message(message.chat.id, "Голос прийнято!")


def finish_election(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    isadmin = False
    admins_t = bot.get_chat_administrators(message.chat.id)
    for admin in admins_t:
        if user_id == admin.user.id:
            isadmin = True
            break
    if not isadmin:
        bot.send_message(message.chat.id, "Ти хто такий шоб сюда тикать, сука? АДМІНА ЗОВИ!!!")
        return
    db_object.execute(f"SELECT elections.userid, d.level, d.username FROM elections JOIN deputats d on elections.userid = d.userid WHERE chatid = CAST({chat_id} AS varchar) ORDER BY votes DESC LIMIT 1")
    result = db_object.fetchone()
    if result is None:
        bot.send_message(message.chat.id, "Ну ти зовсім дебіл, чи хіба трошка?")
        return
    photo = random.randint(0, len(res.level_photos[result[1]]) - 1)
    db_object.execute(f"UPDATE deputats SET level = {result[1] + 1}, photo = {photo} WHERE userid = {result[0]}")
    db_connection.commit()
    bot.send_message(message.chat.id, f"УРА УРА УРА\nВот наш переможець туво є да - {result[2]}")
    bot.send_sticker(message.chat.id, res.happy_sticker)
    db_object.execute(f"DELETE FROM elections WHERE chatid = CAST({chat_id} AS varchar)")
    db_connection.commit()
    db_object.execute(f"DELETE FROM voted WHERE chatid = CAST({chat_id} AS varchar)")
    db_connection.commit()


def _create_buttons_(modifier, message, db_object, bot, price):
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
            buttons.add(types.InlineKeyboardButton
                        (text=res.biz_provide_buttons(result, i, price), callback_data=f'{modifier}{i}'))
    bot.reply_to(message, res.biz_text, reply_markup=buttons)


def visit_business_deputat(message, db_object, bot):
    if message.chat.type != "private":
        bot.reply_to(message, "Команду слід писати в ПП боту!")
        return
    _create_buttons_('vb', message, db_object, bot, False)


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
    today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
    if not result or deputat_id is None or biz_count is None:
        bot.send_message(call.message.chat.id, "І кого ти провідуєш? Мать свою чи шо?")
    elif (today - worked).days < 1:
        bot.send_message(call.message.chat.id, res.biz_worked_text[biz_id])
    elif (today - visited).days >= 7:
        bot.send_message(call.message.chat.id, res.biz_not_visited_text[biz_id])
    else:
        earned = res.biz_profits[biz_id] * random.randint(1, 10) * biz_count
        db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s",
                          (money[0] + earned, user_id))
        db_connection.commit()
        today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
        db_object.execute(f"UPDATE business SET {biz_work} = %s WHERE userid=%s", (today_str, user_id))
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_photos[biz_id], caption=res.biz_work_text[biz_id] + str(earned))


def provide_business_deputat(message, db_object, bot):
    if message.chat.type != "private":
        bot.reply_to(message, "Команду слід писати в ПП боту!")
        return
    _create_buttons_('pb', message, db_object, bot, True)


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
    today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
    days_diff = (today - visited).days
    if not result or deputat_id is None or biz_count is None:
        bot.send_message(call.message.chat.id, "І кого ти провідуєш? Мать свою чи шо?")
    elif visited is not None and days_diff < 7:
        bot.send_message(call.message.chat.id, f"Бізнес не потребує забезпечення, приходьте за {7 - days_diff} дні(-в)")
    elif money[0] < res.biz_provides[biz_id] * biz_count:
        bot.send_message(call.message.chat.id, "В твого депутата замало грошей для підтримання цього бізнесу!")
        bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
    else:
        db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s",
                          (money[0] - res.biz_provides[biz_id] * biz_count, user_id))
        db_connection.commit()
        today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
        db_object.execute(f"UPDATE business SET {biz_visit} = %s WHERE userid=%s", (today_str, user_id))
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_provide_photos[biz_id], caption=res.biz_provide_text[biz_id])


def buy_business_deputat(message, bot):
    if message.chat.type != "private":
        bot.reply_to(message, "Команду слід писати в ПП боту!")
        return
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
    if random.randint(0, 4) == 0:
        db_object.execute(f"SELECT rating FROM deputats WHERE userid = {user_id}")
        result = db_object.fetchone()
        db_object.execute("UPDATE deputats SET rating = %s WHERE userid = %s",
                          (result[0] - res.biz_rating_drop[biz_id], user_id))
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_rating_photo[biz_id], caption=res.biz_rating_text[biz_id])


def handle_biz_purchase_deputat(call, db_object, db_connection, bot):
    user_id = call.from_user.id
    db_object.execute(f"SELECT deputatid, money FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    if not result or result[0] is None:
        bot.send_message(call.message.chat.id, "І кому ти зібрався купляти? Собі чи шо?")
        return
    biz_id = int(call.data[2:3])
    biz_name = res.biz_db_name[biz_id]
    if result[1] < res.biz_prices[biz_id]:
        bot.send_message(call.message.chat.id, "Твій депутат надто бідний, шоб купити о це вот")
        bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
        return
    db_object.execute(f"SELECT kid, negr, kiosk, deputatid FROM business WHERE userid = {user_id}")
    deputat_id = db_object.fetchone()
    if deputat_id is None:
        db_object.execute(f"INSERT INTO business(userid, deputatid, {biz_name})"
                          f" VALUES(%s, %s, 1)", (user_id, result[0]))
        purchase_update(db_connection, db_object, bot, call, result, biz_id, user_id)
    else:
        if deputat_id[biz_id] is None:
            biz_count = 1
        else:
            biz_count = deputat_id[biz_id] + 1
        db_object.execute(
            f"UPDATE business SET {biz_name} = %s, {biz_name + 'visit'} = NULL, {biz_name + 'work'} = NULL WHERE userid = %s",
            (biz_count, user_id))
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


def up_rating_deputat(message, bot):
    if message.chat.type != "private":
        bot.reply_to(message, "Команду слід писати в ПП боту!")
        return
    buttons = types.InlineKeyboardMarkup()
    for i in range(len(res.rating_name)):
        buttons.add(types.InlineKeyboardButton
                    (text=res.rating_name[i] + ' $' + str(res.rating_price[i]), callback_data=f'rt{i}'))
    bot.reply_to(message, "Доступні види підняття рейтингу:", reply_markup=buttons)


def handle_rating_deputat(call, db_object, db_connection, bot):
    user_id = call.from_user.id
    rating = int(call.data[2:3])
    db_object.execute(f"SELECT money, rating, deputatid FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    if result is None or result[2] is None:
        bot.send_message(call.message.chat.id, "У тебе немає депутата")
    elif result[0] < res.rating_price[rating]:
        bot.send_message(call.message.chat.id, "Твоєму депутату не вистачає грошей для цього!")
        bot.send_sticker(call.message.chat.id, res.sad_sticker)
    else:
        db_object.execute(f"UPDATE deputats SET rating = {result[1] + res.rating_up[rating]} WHERE userid = {user_id}")
        db_connection.commit()
        db_object.execute(f"UPDATE deputats SET money = "
                          f"{result[0] - res.rating_price[rating]} WHERE userid = {user_id}")
        db_connection.commit()
        bot.send_message(call.message.chat.id, f"Рейтинг серед громади піднято на {res.rating_up[rating]}⭐️")


def top_deputat(message, db_object, bot):
    db_object.execute("SELECT username, money, rating FROM deputats ORDER BY money DESC LIMIT 30")
    result = db_object.fetchall()
    if not result:
        bot.reply_to(message, "Здається, ніхто навіть не має дупетата...")
    else:
        text = ''
        i = 1
        for row in result:
            text += f"{i} - {row[0]}\n💰{row[1]}$ - ⭐{row[2]}\n"
            i += 1
        bot.reply_to(message, text)


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
