#!/usr/bin/env python3

from collections import Counter
from datetime import datetime
import sys

import pandas as pd
from absl import flags, app

from common import date_is_correct

FLAGS = flags.FLAGS

flags.DEFINE_string('day', None, 'Day of the matchup in format yyyy-mm-dd. If not set, current day will be used')
flags.DEFINE_string('winner', None, 'Name of the winner (player with lower rating value if drawn matchup is adding)')
flags.DEFINE_string('looser', None, 'Name of the looser (player with greater rating value if drawn matchup is adding)')
flags.DEFINE_string('score', None, "Result of match in W:L format (W - winner's won sets, L - looser's won sets)")
flags.DEFINE_string('ball', 'yellow', 'Type of ball used for matchup')
flags.mark_flags_as_required(['winner', 'looser', 'score'])


def check_player(player, games):
    known_players = set(games['Winner'].tolist() + games['Looser'].tolist())
    if player not in known_players:
        print('player {} has no mathups at database, Do you want to add him? ([y]/n)'.format(player))
        confirm = sys.stdin.readline().strip()
        if confirm == 'n':
            print('OK')
            return False
        elif confirm != 'y' and confirm != '':
            print('Response is incorrect')
            return False
        print('Added new player')
        return True
    else:
        return True


def ball_is_correct(ball):
    if not isinstance(ball, str):
        return False
    return ball.lower() in ['yellow', 'blue', 'red']


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
    games_scv_filename = 'games.csv'
    games = pd.read_csv(games_scv_filename)

    game_to_add = {}

    if FLAGS.day is None:
        cur_date = datetime.now()
        cur_year = str(cur_date.year)
        cur_month = '0' * (cur_date.month < 10) + str(cur_date.month)
        cur_day = '0' * (cur_date.day < 10) + str(cur_date.day)
        cur_day_of_year = '{}-{}-{}'.format(cur_year, cur_month, cur_day)
        game_to_add['Date'] = cur_day_of_year
    else:
        if date_is_correct(FLAGS.day):
            game_to_add['Date'] = FLAGS.day
        else:
            print('Entered date is incorrect or has wrong format')
            print('Matchup adding failed')
            return

    played_days = games['Date'].tolist()
    played_days_counts = Counter()
    played_days_counts.update(played_days)
    if game_to_add['Date'] not in played_days_counts.keys():
        game_to_add['Game of the day'] = 1
    else:
        game_to_add['Game of the day'] = played_days_counts[game_to_add['Date']] + 1

    if check_player(FLAGS.winner, games):
        game_to_add['Winner'] = FLAGS.winner
    else:
        print('Matchup adding failed')
        return

    if check_player(FLAGS.looser, games):
        game_to_add['Looser'] = FLAGS.looser
    else:
        print('Matchup adding failed')
        return

    if score_is_correct(FLAGS.score):
        game_to_add['Score'] = FLAGS.score
    else:
        print('Matchup adding failed: score {} is incorrect'.format(FLAGS.score))
        return

    if ball_is_correct(FLAGS.ball):
        game_to_add['Ball'] = FLAGS.ball.lower()
    else:
        print('Matchup adding failed: ball {} is incorrect'.format(FLAGS.ball))
        return

    games = games.append(game_to_add, ignore_index=True)
    games.to_csv(games_scv_filename, index=False)
    print('Matchup adding succeeded')


if __name__ == '__main__':
    app.run(main)
