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


@bot.message_handler(commands=['getDeputat'])
def getDeputat_handler(message):
    id = message.from_user.id
    db_object.execute(f"SELECT userId FROM deputats WHERE userId = {id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO deputats(userId, money, name) VALUES ( %s, %s, %s )", (id, random.randint(0, 100), random.choice(res.deputatNames)))
        db_connection.commit()


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
