#!/usr/bin/env python3

from os import listdir
from os.path import join, splitext, dirname, abspath

import pandas as pd
import numpy as np


active_tournaments = {'LZR Open': 'group stage'}


REPO_ROOT_DIR = join(dirname(abspath(__file__)), '..', '..')
DATA_DIR = abspath(join(REPO_ROOT_DIR, 'data/'))


def extract_games(username, table):
    won = table[table['Winner'] == username]
    lost = table[table['Looser'] == username]
    return {'won': dict(map(tuple, won[['Looser', 'Score']].values)),
            'lost': dict(map(tuple, lost[['Winner', 'Score']].values))}


class Participant:
    def __init__(self, username, table):
        self.name = username
        self.games = extract_games(username, table)

    def __str__(self):
        return str(self.name) + ': ' + str(self.games)


def read_games(data_dir):
    csv_list = list(sorted([join(data_dir, path) for path in listdir(data_dir) if splitext(path)[1] == '.csv']))
    games = pd.concat([pd.read_csv(csv) for csv in csv_list]).reset_index(drop=True)
    return games


def main():
    games = read_games(DATA_DIR)
    games_needed = games[np.logical_and(games['Tournament'] == list(active_tournaments.items())[0][0],
                                        games['Stage'] == list(active_tournaments.items())[0][1])]
    participant_names = list(set(games_needed['Winner']) | set(games_needed['Looser']))
    participants = [Participant(name, games_needed) for name in participant_names]

    participants.sort(key=lambda x: (len(x.games['won']), len(x.games['won']) + len(x.games['lost'])),
                      reverse=True)
    # participants = completesort()

    sorted_names = [participant.name for participant in participants]




    for part in participants:
        print(part)


if __name__ == '__main__':
    main()
