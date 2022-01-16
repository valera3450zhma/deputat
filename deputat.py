import datetime
import random
import res


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
                       caption=f"Перший раз працюєш, да?\n{data[2]}{res.work_text[data[1] - 1]}\n💰 Дохід: ${earned}",
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
        db_object.execute("UPDATE deputats SET level = %s, photo = %s, lastworked = NULL WHERE userid = %s",
                          (result[0] + 1, random.randint(0, len(res.level_photos[result[0]]) - 1), user_id))
        db_connection.commit()
        bot.reply_to(message, "Депутата підвищено до нового рівня! - /show")
        bot.send_sticker(message.chat.id, res.happy_sticker)


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
        bot.reply_to(message, "Депутату розірвало сраку...\nОтримати нового - /get")


def killed_deputats(message, db_object, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT killed FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    if result is None or result[0] is None:
        bot.reply_to(message, "Ти ще не вбивав своїх депутатів")
    else:
        bot.reply_to(message, f"Вбито депутатів: {result[0]}")
