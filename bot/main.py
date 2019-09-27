import telebot
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List

from settings import token, groups, admins, GAME_FORMAT
from utils import format_tags, parse_game

bot = telebot.TeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

@dataclass
class Game:
    user1: str
    score1: int
    score2: int
    user2: str

    def __post_init__(self):
        self.score1 = int(self.score1)
        self.score2 = int(self.score2)

    def str(self):
        return f'@{self.user1} {self.score1}:{self.score2} @{self.user2}'

class Store:
    date = None
    games: List[Game] = None

    @classmethod
    def getInfo(cls):
        day = cls.date.strftime("%d/%m/%Y")
        table = f'{day}:\n\n'
        for (i, game) in enumerate(cls.games, start=1):
            table += f'{i}. {game.str()}\n'
        return table

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
    Store.date = datetime.now()
    Store.games = []
    bot.send_message(message.chat.id, 'Add games with /game command')

@bot.message_handler(commands=['game'])
def game(message):
    if not Store.date:
        bot.reply_to(message, 'First, /start gameday')
        return
    parsed = parse_game(message.text)
    if not parsed:
        bot.reply_to(message, f'Invalid format. Use like: `{GAME_FORMAT}`', parse_mode='markdown')
        return
    Store.games.append(Game(*parsed))
    bot.send_message(message.chat.id, 'Saved! Use /info')

@bot.message_handler(commands=['info'])
def info(message):
    if not Store.date:
        bot.reply_to(message, 'Not started, use /start')
        return
    bot.send_message(message.chat.id, Store.getInfo(), parse_mode='markdown')

bot.polling()
