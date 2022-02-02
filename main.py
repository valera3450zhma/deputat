import datetime
import os

import config
import res
import deputat
import comms.user
import comms.deputat
import comms.biz

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

deput = deputat.Deputat(db_object, db_connection, bot)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, 'ага, ок, запустився я :))')


@bot.message_handler(commands=['me'])
def me_handler(message):
    deput.me(message)


@bot.message_handler(commands=['deputat'])
def deputat_handler(message):
    deput.deputat(message)


@bot.message_handler(commands=['business'])
def business_handler(message):
    deput.business(message)


@bot.message_handler(commands=['elections'])
def elect_deputat_handler(message):
    deput.elections_deputat(message)


@bot.message_handler(commands=['show_candidates'])
def elect_deputat_handler(message):
    deput.show_candidates(message)


@bot.message_handler(commands=['finish_election'])
def elect_deputat_handler(message):
    deput.finish_election(message)


@bot.message_handler(commands=['vote'])
def elect_deputat_handler(message):
    deput.election_vote(message)


@bot.message_handler(commands=['kill'])
def kill_deputat_handler(message):
    deput.kill_deputat(message)


@bot.message_handler(commands=['time'])
def time_deputat_handler(message):
    bot.reply_to(message, str(datetime.datetime.now() + datetime.timedelta(hours=res.hour_adjust)))


@bot.message_handler(commands=['hellp'])
def time_deputat_handler(message):
    bot.reply_to(message, res.help_text)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    data = call.data
    if data == "killed_me":
        comms.user.killed_deputats(deput, call)
    elif data == "top_me":
        comms.user.top_deputat(deput, call)

    elif data == "get_deputat":
        comms.deputat.get_deputat(deput, call)
    elif data == "show_deputat":
        comms.deputat.show_deputat(deput, call)
    elif data == "work_deputat":
        comms.deputat.work_deputat(deput, call)
    elif data == "rating_deputat":
        comms.deputat.up_rating_deputat(deput, call)
    elif data == "lvlup_deputat":
        comms.deputat.lvlup_deputat(deput, call)

    elif data == "collect_business":
        comms.biz.collect_business(deput, call)
    elif data == "provide_business":
        comms.biz.provide_business(deput, call)
    elif data == "buy_business":
        pass
    elif data == "show_business":
        pass

    elif data == "deputat_menu":
        comms.deputat.handle_deputat_menu(deput, call)

    elif data[:2] == "rt":
        comms.deputat.handle_rating_deputat(deput, call)
    elif data[:2] == "cb":
        comms.deputat.handle_rating_deputat(deput, call)
    elif data[:2] == "pb":
        comms.deputat.handle_rating_deputat(deput, call)


@bot.message_handler(commands=['nwork'])
def money_deputat_handler(message):
    if message.from_user.id in res.SU:
        user_id = message.from_user.id
        db_object.execute("UPDATE deputats AS d SET d.last_worked = NULL WHERE d.userid = %s", [user_id])
        db_connection.commit()
        bot.reply_to(message, f"Параметр роботи оновлено. Депутат раніше не працював.")


@bot.message_handler(commands=['nprovide'])
def money_deputat_handler(message):
    if message.from_user.id in res.SU:
        user_id = message.from_user.id
        db_object.execute(f"UPDATE business AS b SET b.last_provided = NULL WHERE b.userid = %s", [user_id])
        db_connection.commit()
        bot.reply_to(message, f"Параметр відвідування оновлено. Депутат раніше не відвідував жоден бізнес.")


@bot.message_handler(commands=['nbusiness'])
def money_deputat_handler(message):
    if message.from_user.id in res.SU:
        user_id = message.from_user.id
        db_object.execute(f"UPDATE business AS b SET b.last_worked = NULL WHERE b.userid = %s", [user_id])
        db_connection.commit()
        bot.reply_to(message, f"Параметр збору оновлено. Депутат раніше не збирав гроші з жодного бізнесу.")


@bot.message_handler(content_types=['text'])
def money_deputat_handler(message):
    if (message.from_user.id in res.SU) and message.text.isnumeric():
        user_id = message.from_user.id
        db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s", (int(message.text), user_id))
        db_connection.commit()
        bot.reply_to(message, f"Параметр гроші оновлено: ${message.text}")


@bot.message_handler(content_types=['photo'])
def send_photo_id(message):
    if message.from_user.id == res.SU[0]:
        bot.reply_to(message, f"{message.photo[len(message.photo) - 1].file_id}")


@bot.message_handler(content_types=['sticker'])
def send_photo_id(message):
    if message.from_user.id == res.SU[0]:
        bot.reply_to(message, message.sticker.file_id)


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
