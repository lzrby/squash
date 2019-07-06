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
GameRatings = namedtuple('GameRatings', ['my', 'opponent'])

FLAGS = flags.FLAGS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT_DIR = os.path.join(SCRIPT_DIR, '..')

flags.DEFINE_string('d', today(), ('Day of leaderboard to print in format yyyy-mm-dd. '
                                   'If day is not specified or its value is equal to today(), '
                                   'script will update json data.'))


def win_set_probability(game_ratings):
    return 1.0 / (1 + 10 ** ((game_ratings.opponent - game_ratings.my) / 400))


def C(k, n):
    return np.math.factorial(n) / np.math.factorial(k) / np.math.factorial(n - k)


def expected_sets_won(game_ratings, n_sets):
    win_prob = win_set_probability(game_ratings)
    sets = np.arange(n_sets + 1)
    win_sets_probs = np.array([C(i, n_sets) * (win_prob ** i) * ((1 - win_prob) ** (n_sets - i)) for i in sets])
    return np.sum(win_sets_probs * sets)


def get_norm_coeff(old_rating, sets_played):
    return 40 if sets_played < constants.SETS_COEFF_BOUND else 10 if old_rating >= constants.RATING_COEFF_BOUND else 20


def update_rating(old_rating, sets_won, sets_won_expected, ball, sets_played):
    norm_coeff = get_norm_coeff(old_rating, sets_played)
    return old_rating + norm_coeff * constants.BALL_COEFFS[ball] * (sets_won - sets_won_expected)


def apply_elo_law(players, score, game_ratings, ball, set_counts):
    won_expected = expected_sets_won(game_ratings, score.winner + score.looser)
    lost_expected = score.winner + score.looser - won_expected
    winner_new_rating = update_rating(game_ratings.my, score.winner, won_expected, ball, set_counts[players.winner])
    looser_new_rating = update_rating(game_ratings.opponent, score.looser,
                                      lost_expected, ball, set_counts[players.looser])
    return GameRatings(winner_new_rating, looser_new_rating)


def update_ratings_with_game(ratings, game, set_counts):
    players = Players(game.Winner, game.Looser)
    score = ScoreInSets(*sorted(map(int, game.Score.split(':')), reverse=True))
    game_ratings = GameRatings(ratings.loc[players.winner].Rating, ratings.loc[players.looser].Rating)

    game_ratings_after = apply_elo_law(players, score, game_ratings, game.Ball, set_counts)
    new_ratings = ratings.copy(deep=True)
    new_ratings.loc[players.winner].Rating = game_ratings_after.my
    new_ratings.loc[players.looser].Rating = game_ratings_after.opponent
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


def get_previous_rating(name, ratings_log):
    days_list = [day for (day, ratings) in ratings_log]
    days_unique_sorted = list(sorted(set(days_list), reverse=True))
    if len(days_unique_sorted) < 2:
        return constants.DEFAULT_RATING
    prev_match_day = days_unique_sorted[1]
    prev_ratings_log_index = len(days_list) - 1 - days_list[::-1].index(prev_match_day)
    prev_ratings = ratings_log[prev_ratings_log_index][1]
    return int(np.round(prev_ratings.loc[name]['Rating']))


def save_ratings_to_json(ratings, ratings_log, set_counts):
    json_data = list(map(lambda name: {'name': name,
                                       'rating': int(np.round(ratings.loc[name]['Rating'])),
                                       'sets': int(set_counts[name]),
                                       'prev_rating': get_previous_rating(name, ratings_log)
                                       }, ratings.index))
    json_filename = os.path.join(REPO_ROOT_DIR, 'leaderboard-ui/src/rating.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
        json_file.write('\n')


def get_ratings_dict(ratings_table):
    return {name: int(np.round(ratings_table.loc[name]['Rating'])) for name in sorted(ratings_table.index)}


def save_ratings_history_to_json(ratings_log):
    json_data = list(map(lambda ratings_log_item: {'date': ratings_log_item[0],
                                                   'ratings': get_ratings_dict(ratings_log_item[1])
                                                   }, ratings_log))
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
