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

class Gameday:
    date = None
    games: List[Game] = None

    @classmethod
    def getDay(cls):
        return cls.date.strftime("%d/%m/%Y")

    @classmethod
    def getInfo(cls):
        table = f'{Gameday.getDay()}:\n\n'
        for (i, game) in enumerate(cls.games, start=1):
            table += f'{i}. {game.str()}\n'
        return table

    @classmethod
    def cleanup(cls):
        cls.date = None
        cls.games = None

    @classmethod
    def init(cls):
        cls.date = datetime.now()
        cls.games = []

    @classmethod
    def is_active(cls):
        return cls.date

def guard(usernames = None, check_is_active = True):
    def inner(func):
        def wrapper(message):
            if not message.chat.id in groups:
                bot.reply_to(message, 'Invalid chat. Use in LZR squash group')
                return
            if usernames and not message.from_user.username in usernames:
                bot.reply_to(message, f'Only {format_tags(usernames)} can call this command')
                return
            if check_is_active and not Gameday.is_active():
                bot.reply_to(message, 'First, /start gameday')
                return
            return func(message)
        return wrapper
    return inner

@bot.message_handler(commands=['forcestart'])
@guard(admins, check_is_active=False)
def _start(message):
    bot.reply_to(message, 'Lets play 🏸🏸🏸!')
    Gameday.init()
    bot.send_message(message.chat.id, 'Add games with /game command')

@bot.message_handler(commands=['start'])
@guard(admins, check_is_active=False)
def start(message):
    if Gameday.is_active() and len(Gameday.games) > 0:
        bot.reply_to(message, f'You have unfinished {Gameday.getDay()} gameday. If you sure - use /forcestart')
        return
    _start(message)

@bot.message_handler(commands=['game'])
@guard()
def game(message):
    parsed = parse_game(message.text)
    if not parsed:
        bot.reply_to(message, f'Invalid format. Use like: `{GAME_FORMAT}`', parse_mode='markdown')
        return
    Gameday.games.append(Game(*parsed))
    bot.send_message(message.chat.id, 'Saved! Use /info')

@bot.message_handler(commands=['info'])
@guard()
def info(message):
    bot.send_message(message.chat.id, Gameday.getInfo(), parse_mode='markdown')

@bot.message_handler(commands=['end'])
@guard(admins)
def end(message):
    bot.reply_to(message, 'TODO: call @klicunou code')

    Gameday.cleanup()

    bot.send_message(message.chat.id, 'Success! 🎉 Check out https://lzrby.github.io/squash')


bot.polling()
