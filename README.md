# squash

🏸 squash club rating tools

## setup

- Install pip(pip3) using your package manager.
- `pip install -r requirements.txt` for required packages.

## scripts

### logger

- Run from terminal at repo root: `./logger.py --winner="Winner Winnerovich" --looser="Looser Looserovich" --score=<winner's sets>:<looser's sets>`.
- `--day` flag is optional (current day is used by default). Day format is yyyy-mm-dd.
- `--ball="<ball color>"` flag is used when play ball was red or blue. Yellow color is default.
- Also see `./logger.py --help`.

### get ratings

- Run from terminal at repo root: `./get_ratings.py --day=<yyyy-mm-dd>`. This scripts prints current ratings for day from input at 23:59:59.
- Also you can see `./get_ratings.py --help`.

### ui

- `npm run deploy` to update rating on [lzrby.github.io/squash](http://lzrby.github.io/squash)
