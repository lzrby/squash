import telebot
import logging
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
import os
from typing import List

from get_ratings import update_json_data
from settings import token, groups, admins, GAME_FORMAT, REPO_ROOT_DIR, DATA_DIR
from utils import add_result, format_tags, parse_game, commit

bot = telebot.TeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


def get_diffs_table(diffs):
    table = ''
    for (diff, name) in diffs:
        table += f'- @{name}: {"+" if diff > 0 else ""}{diff}\n'
    return table


@dataclass
class Game:
    user1: str
    score1: int
    score2: int
    user2: str
    tournament: str
    stage: str

    def __post_init__(self):
        self.score1 = int(self.score1)
        self.score2 = int(self.score2)
        self.user1 = self.user1.lower()
        self.user2 = self.user2.lower()

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


def guard(usernames=None, check_is_active=True):
    def inner(func):
        def wrapper(message):
            if message.chat.id not in groups:
                bot.reply_to(message, 'Invalid chat. Use in LZR squash group')
                return
            if usernames and message.from_user.username not in usernames:
                bot.reply_to(message, f'Only {format_tags(usernames)} can call this command', disable_notification=True)
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
    Gameday.games.append(Game(*parsed, None, None))
    bot.send_message(message.chat.id, 'Saved! Use /info')


@bot.message_handler(commands=['tourngame'])
@guard()
def tournament_ggame(message):
    active_tournaments = {'LZR Open': 'group stage'}

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    item_buttons = [telebot.types.KeyboardButton(tournament) for tournament in active_tournaments]
    markup.add(*item_buttons)
    bot.send_message(message.chat.id, "Choose the tournament:", reply_markup=markup)


@bot.message_handler(commands=['info'])
@guard()
def info(message):
    bot.send_message(message.chat.id, Gameday.getInfo(), disable_notification=True)


@bot.message_handler(commands=['end'])
@guard(admins)
def end(message):
    if not len(Gameday.games):
        bot.reply_to(message, 'No games, add with /game command, or /start to reset')
        Gameday.init()
        return
    csv_path_to_save = os.path.join(DATA_DIR, f'{Gameday.date.strftime("%Y")}.csv')
    dataframe_to_save = pd.DataFrame(columns=['Date', 'Index', 'Winner', 'Looser', 'Score', 'Tournament', 'Stage'])
    if os.path.isfile(csv_path_to_save):
        dataframe_to_save = pd.read_csv(csv_path_to_save)
    for result in Gameday.games:
        dataframe_to_save = add_result(dataframe_to_save,
                                       result.user1, result.user2,
                                       result.score1, result.score2,
                                       result.tournament, result.stage,
                                       Gameday.date)
    dataframe_to_save.to_csv(csv_path_to_save, index=False)
    diffs = update_json_data()
    commit(Gameday.getDay())

    Gameday.cleanup()

    bot.send_message(message.chat.id, f'Success! 🎉\n\n{get_diffs_table(diffs)}\nCheck out https://lzrby.github.io/squash', disable_notification=True)


bot.polling()
