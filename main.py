import os
import random

import telebot
from flask import Flask, request

TOKEN = '5096572615:AAFa9UR2veKN2VoHSpftGR6C0uD98VF6spo'
APP_URL = f'https://deputatbot.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def commands_handler(message):
    bot.reply_to(message, 'ага, ок, запустився я :))')


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
