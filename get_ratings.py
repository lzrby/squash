#!/usr/bin/env python3

import numpy as np
import pandas as pd
from absl import flags, app

from common import date_is_correct

FLAGS = flags.FLAGS

flags.DEFINE_string('day', None, 'Day of the matchup in format yyyy-mm-dd.')
flags.mark_flag_as_required('day')


def win_set_probability(my_rating, opponent_rating):
    return 1.0 / (1 + 10 ** ((opponent_rating - my_rating) / 400))


def binom_coeff(k, n):
    return np.math.factorial(n) / np.math.factorial(k) / np.math.factorial(n - k)


def expected_sets_won(my_rating, opponent_rating, n_sets):
    win_probability = win_set_probability(my_rating, opponent_rating)
    win_sets_probabilities = np.array([binom_coeff(i, n_sets) * (win_probability ** i) * ((1 - win_probability) ** (n_sets - i)) for i in range(n_sets + 1)])
    sets_counts = np.arange(n_sets + 1)
    return np.sum(win_sets_probabilities * sets_counts)


def count_new_rating(old_rating, expected_sets_won, real_sets_won, ball_coeff):
    norm_coeff = 10 if old_rating >= 2400 else 20
    return old_rating + norm_coeff * ball_coeff * (real_sets_won - expected_sets_won)


def apply_elo_law(winner, looser,
                  winner_sets, looser_sets,
                  ball_coeff,
                  winner_rating, looser_rating):
    total_sets = winner_sets + looser_sets
    won_expected = expected_sets_won(winner_rating, looser_rating, total_sets)
    lost_expected = total_sets - won_expected
    winner_new_rating = count_new_rating(winner_rating, won_expected, winner_sets, ball_coeff)
    looser_new_rating = count_new_rating(looser_rating, lost_expected, looser_sets, ball_coeff)
    return winner_new_rating, looser_new_rating


def update_ratings_with_game(ratings, game):
    winner = game.Winner
    looser = game.Looser

    sets = list(map(int, game.Score.split(':')))

    winner_sets = np.max(sets)
    looser_sets = np.min(sets)

    ball_coeffs = {'blue':0.5, 'red':0.7, 'yellow':1.0}
    ball_coeff = ball_coeffs[game.Ball]

    winner_rating = ratings.loc[winner].Rating
    looser_rating = ratings.loc[looser].Rating

    winner_new_rating, looser_new_rating = apply_elo_law(winner, looser,
                                                         winner_sets, looser_sets,
                                                         ball_coeff,
                                                         winner_rating, looser_rating)
    ratings.loc[winner].Rating = winner_new_rating
    ratings.loc[looser].Rating = looser_new_rating



def count_ratings(date):
    games = pd.read_csv('games.csv')
    sorted_games = games.sort_values(['Date', 'Game of the day'])
    proper_games = sorted_games[sorted_games['Date'] < date]
    all_players = list(set(proper_games['Winner'].tolist() + proper_games['Looser'].tolist()))
    data = {'Rating':[1400.00 for i in range(len(all_players))]}
    result = pd.DataFrame(data, index=all_players)
    n_games = proper_games.shape[0]
    for i in range(n_games):
        update_ratings_with_game(result, proper_games.loc[i])
    result = result.sort_values(['Rating'], ascending=False)
    return result


def main(_):
    if not date_is_correct(FLAGS.day):
        print('Date is incorrect or it has wrong format')
        return
    ratings = count_ratings(FLAGS.day)
    print(ratings)


if __name__ == '__main__':
    app.run(main)
