#!/usr/bin/env python3

from collections import Counter
from datetime import datetime
import os

from absl import flags, app
import pandas as pd


FLAGS = flags.FLAGS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT_DIR = os.path.join(SCRIPT_DIR, '..')

flags.DEFINE_string('w', None, 'Name of the winner (player with lower rating value if drawn matchup is adding).')
flags.DEFINE_string('l', None, 'Name of the looser (player with greater rating value if drawn matchup is adding).')
flags.DEFINE_string('s', None, "Result of match in W:L format (W - winner's won sets, L - looser's won sets).")
flags.mark_flags_as_required(['w', 'l', 's'])


def today():
    return datetime.now().strftime("%Y-%m-%d")


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

    if not score_is_correct(FLAGS.s):
        print('Matchup adding failed: score {} is incorrect'.format(FLAGS.s))
        return

    new_game = {'Date': today(), 'Winner': FLAGS.w, 'Looser': FLAGS.l, 'Score': FLAGS.s}
    day_games = Counter(games['Date'].tolist())
    new_game['Index'] = 1 if new_game['Date'] not in day_games.keys() else day_games[new_game['Date']] + 1

    games = games.append(new_game, ignore_index=True)
    games.to_csv(games_csv_filepath, index=False)
    print('Matchup adding succeeded')


if __name__ == '__main__':
    app.run(main)
