import random
import sys
import res


def get_deputat(message, db_object, db_connection, bot):
    user_id = message.from_user.id
    db_object.execute(f"SELECT userid, deputatid FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()
    db_object.execute("SELECT deputatid FROM deputats WHERE deputatid IS NOT NULL ORDER BY deputatid DESC LIMIT 1")
    last_deputat = db_object.fetchone()
    if result is None:
        if last_deputat is None:
            deputat_id = -(sys.maxsize - 1)
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
            deputat_id = -(sys.maxsize - 1)
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
