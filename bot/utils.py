from collections import Counter as _counter
import re

# https://regex101.com/r/9dIo49/2
GAME_REGEX = r'/game @([^\s]+) (\d+):(\d+) @([^\s]+)'


def add_result(games, player1, player2, score1, score2, date):
    new_game = {'Date': date.strftime("%Y-%m-%d"),
                'Winner': player1 if score1 > score2 else player2,
                'Looser': player2 if score1 > score2 else player1,
                'Score': f'{score1}:{score2}' if score1 > score2 else f'{score2}:{score1}'}
    day_games = _counter(games['Date'].tolist())
    new_game['Index'] = 1 if new_game['Date'] not in day_games.keys() else day_games[new_game['Date']] + 1
    return games.append(new_game, ignore_index=True)


def format_tags(usernames):
    return ', '.join([f'@{u}' for u in usernames])


def parse_game(text):
    match = re.search(GAME_REGEX, text)
    if not match:
        return None
    return match.groups()
