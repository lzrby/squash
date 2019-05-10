#!/usr/bin/env python3

from datetime import datetime
import json
import os

from absl import flags, app
import numpy as np
import pandas as pd

from common import date_is_correct
import constants

FLAGS = flags.FLAGS
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root_dir = os.path.join(script_dir, '..')

flags.DEFINE_string('day', None, 'Day of leaderboard in format yyyy-mm-dd.')


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
    if sets_played < 100:
        return 40
    elif old_rating >= 2400:
        return 10
    else:
        return 20


def count_new_rating(old_rating, expected_sets_won, real_sets_won, ball_coeff, sets_played):
    norm_coeff = get_norm_coeff(old_rating, sets_played)
    return old_rating + norm_coeff * ball_coeff * (real_sets_won - expected_sets_won)


def apply_elo_law(winner, looser, winner_sets, looser_sets, ball_coeff, winner_rating, looser_rating, set_counts):
    total_sets = winner_sets + looser_sets
    won_expected = expected_sets_won(winner_rating, looser_rating, total_sets)
    lost_expected = total_sets - won_expected
    winner_new_rating = count_new_rating(winner_rating, won_expected, winner_sets, ball_coeff, set_counts[winner])
    looser_new_rating = count_new_rating(looser_rating, lost_expected, looser_sets, ball_coeff, set_counts[looser])
    return winner_new_rating, looser_new_rating


def update_ratings_with_game(ratings, game, set_counts):
    winner = game.Winner
    looser = game.Looser
    sets = list(map(int, game.Score.split(':')))

    winner_sets = np.max(sets)
    looser_sets = np.min(sets)
    ball_coeff = constants.BALL_COEFFS[game.Ball]
    winner_rating = ratings.loc[winner].Rating
    looser_rating = ratings.loc[looser].Rating

    winner_new_rating, looser_new_rating = apply_elo_law(winner, looser, winner_sets, looser_sets,
                                                         ball_coeff, winner_rating, looser_rating, set_counts)
    new_ratings = ratings.copy(deep=True)
    new_ratings.loc[winner].Rating = winner_new_rating
    new_ratings.loc[looser].Rating = looser_new_rating
    total_sets = winner_sets + looser_sets
    set_counts[winner] += total_sets
    set_counts[looser] += total_sets
    return new_ratings


def count_ratings(date):
    game_data_filepath = os.path.join(repo_root_dir, 'data/games.csv')
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
    json_list = [{'name': name,
                  'rating': int(np.round(ratings.loc[name]['Rating'])),
                  'sets': int(set_counts[name])} for name in ratings.index]
    json_filename = os.path.join(repo_root_dir, 'leaderboard-ui/src/rating.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_list, json_file, indent=2)
        json_file.write('\n')


def save_ratings_history_to_json(ratings_log):
    json_list = []
    for (date, ratings) in ratings_log:
        ratings_dict = {name: int(np.round(ratings.loc[name]['Rating'])) for name in ratings.index}
        json_list.append({'date': date, 'ratings': ratings_dict})
    json_filename = os.path.join(repo_root_dir, 'leaderboard-ui/src/ratings_history.json')
    with open(json_filename, 'w') as json_file:
        json.dump(json_list, json_file, indent=2)
        json_file.write('\n')


def main(_):
    if FLAGS.day is None:
        cur_date = datetime.now()
        cur_year = str(cur_date.year)
        cur_month = '0' * (cur_date.month < 10) + str(cur_date.month)
        cur_day = '0' * (cur_date.day < 10) + str(cur_date.day)
        cur_day_of_year = '{}-{}-{}'.format(cur_year, cur_month, cur_day)
        ratings, ratings_log, set_counts = count_ratings(cur_day_of_year)
        save_ratings_to_json(ratings, ratings_log, set_counts)
        save_ratings_history_to_json(ratings_log)
        print(set_counts)
    elif not date_is_correct(FLAGS.day):
        print('Date is incorrect or it has wrong format')
    else:
        ratings, ratings_log, set_counts = count_ratings(FLAGS.day)
        save_ratings_to_json(ratings, ratings_log, set_counts)
        save_ratings_history_to_json(ratings_log)


if __name__ == '__main__':
    app.run(main)
