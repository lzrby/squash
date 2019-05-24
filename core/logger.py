#!/usr/bin/env python3

from collections import Counter
import os
import sys

from absl import flags, app
import pandas as pd

from common import date_is_correct, today
import constants

FLAGS = flags.FLAGS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT_DIR = os.path.join(SCRIPT_DIR, '..')

flags.DEFINE_string('d', today(), 'Day of the matchup in format yyyy-mm-dd. If not set, current day will be used')
flags.DEFINE_string('w', None, 'Name of the winner (player with lower rating value if drawn matchup is adding)')
flags.DEFINE_string('l', None, 'Name of the looser (player with greater rating value if drawn matchup is adding)')
flags.DEFINE_string('s', None, "Result of match in W:L format (W - winner's won sets, L - looser's won sets)")
flags.DEFINE_string('b', 'yellow', 'Type of ball used for matchup')
flags.mark_flags_as_required(['w', 'l', 's'])


def check_player(player, games):
    known_players = set(games['Winner'].tolist() + games['Looser'].tolist())
    if player not in known_players:
        print('player {} has no mathups at database, Do you want to add him? ([y]/n)'.format(player))
        confirm = sys.stdin.readline().strip()
        if confirm == 'n' or confirm not in ['y', '']:
            print('Player adding aborted')
            return False
        print('Added new player')
    return True


def ball_is_correct(ball):
    if not isinstance(ball, str):
        return False
    return ball.lower() in ['yellow', 'blue', 'red', 'y', 'b', 'r']


def score_is_correct(score):
    if not isinstance(score, str):
        return False
    score_items = score.split(':')
    if len(score_items) != 2:
        return False
    for score_item in score_items:
        if not score_item.isdigit() or int(score_item) < 0:
            return False
    return True


def main(_):
    games_csv_filepath = os.path.join(REPO_ROOT_DIR, 'data/games.csv')
    games = pd.read_csv(games_csv_filepath)

    if not date_is_correct(FLAGS.d):
        print('Matchup adding failed: entered date {} is incorrect or has wrong format'.format(FLAGS.d))
        return
    if not check_player(FLAGS.w, games) or not check_player(FLAGS.l, games):
        print('Matchup adding failed because of player adding fail')
        return
    if not score_is_correct(FLAGS.s):
        print('Matchup adding failed: score {} is incorrect'.format(FLAGS.s))
        return
    if not ball_is_correct(FLAGS.b):
        print('Matchup adding failed: ball {} is incorrect'.format(FLAGS.b))
        return

    new_game = {'Date': FLAGS.d, 'Winner': FLAGS.w, 'Looser': FLAGS.l, 'Score': FLAGS.s}
    day_games = Counter(games['Date'].tolist())
    new_game['Game of the day'] = 1 if new_game['Date'] not in day_games.keys() else day_games[new_game['Date']] + 1
    new_game['Ball'] = constants.BALLS[FLAGS.b] if FLAGS.b in constants.BALLS else FLAGS.b.lower()

    games = games.append(new_game, ignore_index=True)
    games.to_csv(games_csv_filepath, index=False)
    print('Matchup adding succeeded')


if __name__ == '__main__':
    app.run(main)
