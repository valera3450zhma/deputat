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
def getDeputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT userid FROM deputats WHERE userid = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO deputats(userid, money, name, level, photo) VALUES ( %s, %s, %s, %s, %s )", (user_id, random.randint(10, 100), random.choice(res.deputatNames), 1, random.randint(0, len(res.level1_photos)-1)))
        db_connection.commit()
        bot.reply_to(message, "Гля який! Депута-а-атіще! Хочеш глянуть на підарасіка? Цикай - /show")
    else:
        bot.reply_to(message, "Так ти вже маєш депутата...")


@bot.message_handler(commands=['show'])
def showDeputat_handler(message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT name, money, level, photo FROM deputats WHERE deputats.userid = {user_id}")
    result = db_object.fetchone()
    if not result:
        bot.reply_to(message, "Ніхуя нема...")
    else:
        reply_message = ""
        deputat_photo = res.level1_photos[result[3]]
        reply_message += f"👨🏻 Ім'я: {result[0]}\n💰 Бабло: {result[1]}\n📚 Рівень: {result[2]}"
        bot.send_photo(message.chat.id, deputat_photo, reply_to_message_id=message.id, caption=reply_message)


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
