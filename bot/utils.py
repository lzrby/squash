from git import Repo, Actor
from collections import Counter as _counter
import re


def add_result(games, player1, player2, score1, score2, tournament, stage, date):
    looser, winner = sorted([(score1, player1), (score2, player2)])
    new_game = {'Date': date.strftime("%Y-%m-%d"),
                'Winner': winner[1],
                'Looser': looser[1],
                'Score': f'{winner[0]}:{looser[0]}',
                'Tournament': tournament,
                'Stage': stage}
    day_games = _counter(games['Date'].tolist())
    new_game['Index'] = 1 if new_game['Date'] not in day_games.keys() else day_games[new_game['Date']] + 1
    return games.append(new_game, ignore_index=True)


def format_tags(usernames):
    return ', '.join([f'@{u}' for u in usernames])


def parse_game(text):
    # https://regex101.com/r/9dIo49/3
    game_regex = r'/(?:tourngame|game) @([^\s]+) (\d+):(\d+) @([^\s]+)'
    match_game = re.search(game_regex, text)
    if not match_game:
        return None
    return match_game.groups()


def commit(date):
    repo = Repo(search_parent_directories=True)

    author = Actor('wirbot', 'wir.development@gmail.com')
    committer = Actor('wirbot', 'wir.development@gmail.com')

    repo.git.add('.')
    repo.index.commit(f'Updates: {date}', author=author, committer=committer)

    repo.git.push()
