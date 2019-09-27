import re

# https://regex101.com/r/9dIo49/1
GAME_REGEX = r'/game @([^\s]+) (\d+)-(\d+) @([^\s]+)'

def format_tags(usernames):
    return ', '.join([f'@{u}' for u in usernames])

def parse_game(text):
    match = re.search(GAME_REGEX, text)
    if not match:
        return None
    return match.groups()
