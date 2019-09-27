import telebot
import logging

from settings import token, groups, admins
from utils import format_tags

bot = telebot.TeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

def guard(usernames = None):
    def inner(func):
        def wrapper(message):
            if not message.chat.id in groups:
                bot.reply_to(message, 'Invalid chat. Use in LZR squash group')
                return
            if usernames and not message.from_user.username in usernames:
                bot.reply_to(message, f'Only {format_tags(usernames)} can call this command')
                return
            return func(message)
        return wrapper
    return inner

@bot.message_handler(commands=['start'])
@guard(admins)
def start(message):
    bot.reply_to(message, 'Lets play 🏸🏸🏸!')


bot.polling()
