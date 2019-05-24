#!/usr/bin/env python3

from collections import namedtuple
import json
import os

from absl import flags, app
import numpy as np
import pandas as pd

from common import date_is_correct, today
import constants

Players = namedtuple('Players', ['winner', 'looser'])
ScoreInSets = namedtuple('Score', ['winner', 'looser'])

FLAGS = flags.FLAGS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT_DIR = os.path.join(SCRIPT_DIR, '..')

flags.DEFINE_string('d', today(), 'Day of leaderboard in format yyyy-mm-dd.')


def win_set_probability(my_rating, opponent_rating):
    return 1.0 / (1 + 10 ** ((opponent_rating - my_rating) / 400))


def C(k, n):
    return np.math.factorial(n) / np.math.factorial(k) / np.math.factorial(n - k)


def expected_sets_won(my_rating, opponent_rating, n_sets):
    win_prob = win_set_probability(my_rating, opponent_rating)
    sets = np.arange(n_sets + 1)
    win_sets_probs = np.array([C(i, n_sets) * (win_prob ** i) * ((1 - win_prob) ** (n_sets - i)) for i in sets])
    return np.sum(win_sets_probs * sets)


def get_norm_coeff(old_rating, sets_played):
    return 40 if sets_played < 100 else 10 if old_rating >= 2400 else 20


def update_rating(old_rating, sets_won_expected, sets_won, ball, sets_played):
    norm_coeff = get_norm_coeff(old_rating, sets_played)
    return old_rating + norm_coeff * constants.BALL_COEFFS[ball] * (sets_won - sets_won_expected)


def apply_elo_law(players, score, winner_rating, looser_rating, ball, set_counts):
    won_expected = expected_sets_won(winner_rating, looser_rating, score.winner + score.looser)
    lost_expected = score.winner + score.looser - won_expected
    winner_new_rating = update_rating(winner_rating, won_expected, score.winner, ball, set_counts[players.winner])
    looser_new_rating = update_rating(looser_rating, lost_expected, score.looser, ball, set_counts[players.looser])
    return winner_new_rating, looser_new_rating


def update_ratings_with_game(ratings, game, set_counts):
    players = Players(game.Winner, game.Looser)
    score = ScoreInSets(*sorted(list(map(int, game.Score.split(':'))), reverse=True))
    winner_rating = ratings.loc[players.winner].Rating
    looser_rating = ratings.loc[players.looser].Rating

    winner_new_rating, looser_new_rating = apply_elo_law(players, score, winner_rating, looser_rating, game.Ball, set_counts)
    new_ratings = ratings.copy(deep=True)
    new_ratings.loc[players.winner].Rating = winner_new_rating
    new_ratings.loc[players.looser].Rating = looser_new_rating
    set_counts[players.winner] += score.winner + score.looser
    set_counts[players.looser] += score.winner + score.looser
    return new_ratings


def count_ratings(date):
    game_data_filepath = os.path.join(REPO_ROOT_DIR, 'data/games.csv')
    games = pd.read_csv(game_data_filepath)
    sorted_games = games.sort_values(['Date', 'Game of the day'])
    proper_games = sorted_games[sorted_games['Date'] <= date]

    all_players = list(set(proper_games['Winner'].tolist() + proper_games['Looser'].tolist()))
    data = {'Rating': [constants.DEFAULT_RATING for i in range(len(all_players))]}
    start_ratings = pd.DataFrame(data, index=all_players)
    n_games = proper_games.shape[0]
    set_counts = {name: 0 for name in all_players}
    ratings_log = [(proper_games.loc[0]['Date'], start_ratings)]

    for i in range(n_games):
        new_ratings = update_ratings_with_game(ratings_log[-1][1], proper_games.loc[i], set_counts)
        new_ratings = new_ratings.sort_values(['Rating'], ascending=False)
        ratings_log.append((proper_games.loc[i]['Date'], new_ratings.copy(deep=True)))
    return ratings_log[-1][1], ratings_log, set_counts


def save_ratings_to_json(ratings, ratings_log, set_counts):
    json_data = []
    for name in ratings.index:
        dict_to_save = {'name': name,
                        'rating': int(np.round(ratings.loc[name]['Rating'])),
                        'sets': int(set_counts[name])}
        for i in range(len(ratings_log)):
            cur_day, cur_ratings = ratings_log[i]
            if cur_day == ratings_log[-1][0]:
                if i != 0:
                    prev_day, prev_ratings = ratings_log[i-1]
                    dict_to_save['prev_rating'] = int(np.round(prev_ratings.loc[name]['Rating']))
                else:
                    dict_to_save['prev_rating'] = int(np.round(cur_ratings.loc[name]['Rating']))
                break
        json_data.append(dict_to_save)
    json_filename = os.path.join(REPO_ROOT_DIR, 'leaderboard-ui/src/rating.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
        json_file.write('\n')


def save_ratings_history_to_json(ratings_log):
    json_data = []
    for (date, ratings) in ratings_log:
        ratings_dict = {name: int(np.round(ratings.loc[name]['Rating'])) for name in sorted(ratings.index)}
        json_data.append({'date': date, 'ratings': ratings_dict})
    json_filename = os.path.join(REPO_ROOT_DIR, 'leaderboard-ui/src/ratings_history.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
        json_file.write('\n')


def main(_):
    if FLAGS.d == today():
        ratings, ratings_log, set_counts = count_ratings(FLAGS.d)
        save_ratings_to_json(ratings, ratings_log, set_counts)
        save_ratings_history_to_json(ratings_log)
    elif not date_is_correct(FLAGS.d):
        print('Date is incorrect or it has wrong format')
    else:
        ratings, ratings_log, set_counts = count_ratings(FLAGS.d)
        print(ratings)


if __name__ == '__main__':
    app.run(main)
