#!/usr/bin/env python3

from collections import namedtuple
import json
import os

import numpy as np
import pandas as pd


GameRatings = namedtuple('GameRatings', ['my', 'opponent'])
Players = namedtuple('Players', ['winner', 'looser'])
ScoreInSets = namedtuple('Score', ['winner', 'looser'])
Sets = namedtuple('Sets', ['total', 'won'])

DEFAULT_RATING = 1400.00
RATING_COEFF_BOUND = 2400.00
SETS_COEFF_BOUND = 300

REPO_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


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
    return 40 if sets_played < SETS_COEFF_BOUND else 10 if old_rating >= RATING_COEFF_BOUND else 20


def update_rating(old_rating, sets_won, sets_won_expected, sets_played):
    norm_coeff = get_norm_coeff(old_rating, sets_played)
    return old_rating + norm_coeff * (sets_won - sets_won_expected)


def apply_elo_law(players, score, game_ratings, set_counts):
    won_expected = expected_sets_won(game_ratings, score.winner + score.looser)
    lost_expected = score.winner + score.looser - won_expected
    winner_new_rating = update_rating(game_ratings.my, score.winner,
                                      won_expected, set_counts[players.winner].total)
    looser_new_rating = update_rating(game_ratings.opponent, score.looser,
                                      lost_expected, set_counts[players.looser].total)
    return GameRatings(winner_new_rating, looser_new_rating)


def update_ratings_with_game(ratings, game, set_counts):
    players = Players(game.Winner, game.Looser)
    score = ScoreInSets(*sorted(map(int, game.Score.split(':')), reverse=True))
    game_ratings = GameRatings(ratings.loc[players.winner].Rating, ratings.loc[players.looser].Rating)

    game_ratings_after = apply_elo_law(players, score, game_ratings, set_counts)
    new_ratings = ratings.copy(deep=True)
    new_ratings.loc[players.winner].Rating = game_ratings_after.my
    new_ratings.loc[players.looser].Rating = game_ratings_after.opponent
    set_counts[players.winner] = Sets(set_counts[players.winner].total + score.looser + score.winner,
                                      set_counts[players.winner].won + score.winner)
    set_counts[players.looser] = Sets(set_counts[players.looser].total + score.looser + score.winner,
                                      set_counts[players.looser].won + score.looser)
    return new_ratings


def count_ratings(games):
    proper_games = games.sort_values(['Date', 'Index'])

    all_players = list(set(proper_games['Winner'].tolist() + proper_games['Looser'].tolist()))
    data = {'Rating': [DEFAULT_RATING for i in range(len(all_players))]}
    start_ratings = pd.DataFrame(data, index=all_players)
    n_games = proper_games.shape[0]
    set_counts = {name: Sets(0, 0) for name in all_players}
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
        return DEFAULT_RATING
    prev_match_day = days_unique_sorted[1]
    prev_ratings_log_index = len(days_list) - 1 - days_list[::-1].index(prev_match_day)
    prev_ratings = ratings_log[prev_ratings_log_index][1]
    return int(np.round(prev_ratings.loc[name]['Rating']))


def save_ratings_to_json(ratings, ratings_log, set_counts):
    json_data = list(map(lambda name: {'name': name,
                                       'rating': int(np.round(ratings.loc[name]['Rating'])),
                                       'sets': int(set_counts[name].total),
                                       'sets_won': int(set_counts[name].won),
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


def update_json_data(games):
    ratings, ratings_log, set_counts = count_ratings(games)
    save_ratings_to_json(ratings, ratings_log, set_counts)
    save_ratings_history_to_json(ratings_log)


if __name__ == '__main__':
    game_data_filepath = os.path.join(REPO_ROOT_DIR, 'data/games.csv')
    games = pd.read_csv(game_data_filepath)
    update_json_data(games)
