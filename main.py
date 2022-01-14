import datetime
import os
import random

import config
import res

import telebot
import logging
import psycopg2
from flask import Flask, request

bot = telebot.TeleBot(config.TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(config.DB_URI, sslmode='require')
db_object = db_connection.cursor()


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, 'ага, ок, запустився я :))')


@bot.message_handler(commands=['get'])
def get_deputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT userid FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute(
            "INSERT INTO deputats(userid, money, name, level, photo, username) VALUES ( %s, %s, %s, %s, %s, %s )", (
                user_id, random.randint(10, 100), random.choice(res.deputatNames), 1,
                random.randint(0, len(res.level_photos[0]) - 1), message.from_user.first_name))
        db_connection.commit()
        bot.reply_to(message, "Гля який! Депута-а-атіще! Хочеш глянуть на підарасіка? Цикай - /show")
    else:
        bot.reply_to(message, "Так ти вже маєш депутата...")


@bot.message_handler(commands=['show'])
def show_deputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT name, money, level, photo FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result:
        bot.reply_to(message, "Ніхуя нема...")
    else:
        reply_message = ""
        deputat_photo = res.level_photos[result[2] - 1][result[3]]
        reply_message += f"👨🏻 Ім'я: {result[0]}\n💰 Бабло: ${result[1]}\n📚 Рівень: {result[2]} " \
                         f"- {res.level_captions[result[2] - 1]} "
        bot.send_photo(message.chat.id, deputat_photo, reply_to_message_id=message.id, caption=reply_message)


@bot.message_handler(commands=['work'])
def work_deputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT lastworked FROM deputats WHERE deputats.userid = {user_id}")
    last_worked = db_object.fetchone()
    db_object.execute(f"SELECT money, level, name FROM deputats WHERE deputats.userid = {user_id}")
    data = db_object.fetchone()
    if not last_worked:
        bot.reply_to(message, "В тебе нема депутата, шоб він працював")
    elif not last_worked[0]:
        today_str = datetime.datetime.today().strftime("%Y-%m-%d")
        earned = random.randint(10, 100) * res.money_earn_multiplier[data[1] - 1]
        db_object.execute("UPDATE deputats SET lastworked = %s, money = %s WHERE userid = %s",
                          (today_str, int(data[0]) + earned, user_id))
        db_connection.commit()
        bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                       caption=data[2] + res.work_text + "\n💰 Дохід: $" + data[0], reply_to_message_id=message.id)

    else:
        worked = datetime.datetime(last_worked[0][0:4], last_worked[0][5:7], last_worked[0][8:10])
        today = datetime.datetime.today()
        if (today - worked).days >= 1:
            today_str = datetime.datetime.today().strftime("%Y-%m-%d")
            earned = random.randint(10, 100) * res.money_earn_multiplier[data[1] - 1]
            db_object.execute("UPDATE deputats SET lastworked = %s, money = %s WHERE userid = %s",
                              (today_str, int(data[0]) + earned, user_id))
            db_connection.commit()
            bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                           caption=data[2] + res.work_text + "\n💰 Дохід: $" + data[0])
        else:
            bot.send_photo(message.chat.id, random.choice(res.not_working_photos),
                           caption="Твій депутат вже заїбався бо нині відхуячив своє", reply_to_message_id=message.id)


@bot.message_handler(commands=['lvlup'])
def kill_deputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT level FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result:
        bot.reply_to(message, "А шо апати то?")
    elif result[0] == res.MAX_LEVEL:
        bot.reply_to(message, "В депутата максимальний рівень!")
    else:
        db_object.execute("UPDATE deputats SET level = %s, photo = %s WHERE userid = %s",
                          (result[0] + 1, random.randint(0, len(res.level_photos[result[0]]) - 1), user_id))
        db_connection.commit()
        bot.reply_to(message, "Депутата підвищено до нового рівня! - /show")


@bot.message_handler(commands=['kill'])
def kill_deputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT name FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result:
        bot.reply_to(message, "А шо вбивати то?")
    else:
        db_object.execute("DELETE FROM deputats WHERE userid = %s", [user_id])
        db_connection.commit()
        bot.reply_to(message, "Депутату розірвало сраку...")


@bot.message_handler(content_types=['photo'])
def send_photo_id(message):
    if message.from_user.id == 506126580:
        bot.reply_to(message, f"{message.photo[len(message.photo) - 1].file_id}")


@server.route('/' + config.TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
