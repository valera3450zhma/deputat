import datetime
import os

import config
import res
import deputat

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
    deputat.get_deputat(message, db_object, db_connection, bot)


@bot.message_handler(commands=['show'])
def show_deputat_handler(message):
    deputat.show_deputat(message, db_object, bot)


@bot.message_handler(commands=['work'])
def work_deputat_handler(message):
    deputat.work_deputat(message, db_object, db_connection, bot)


@bot.message_handler(commands=['lvlup'])
def kill_deputat_handler(message):
    deputat.lvlup_deputat(message, db_object, db_connection, bot)


@bot.message_handler(commands=['kill'])
def kill_deputat_handler(message):
    deputat.kill_deputat(message, db_object, db_connection, bot)


@bot.message_handler(commands=['killed'])
def time_deputat_handler(message):
    deputat.killed_deputats(message, db_object, bot)


@bot.message_handler(commands=['time'])
def time_deputat_handler(message):
    bot.reply_to(message, str(datetime.datetime.now()))


@bot.message_handler(commands=['did_not_work'])
def money_deputat_handler(message):
    if message.from_user.id == res.SU[0] or message.from_user.id == res.SU[1]:
        user_id = message.from_user.id
        db_object.execute("UPDATE deputats SET lastworked = NULL WHERE userid = %s", [user_id])
        db_connection.commit()
        bot.reply_to(message, f"Параметр роботи оновлено. Депутат раніше не працював.")


@bot.message_handler(content_types=['text'])
def money_deputat_handler(message):
    if (message.from_user.id == res.SU[0] or message.from_user.id == res.SU[1]) and message.text.isnumeric():
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
