# squash

🏸 squash club rating tools

## setup

- Install pip(pip3) using your package manager.
- `pip install -r requirements.txt` for required packages.

## scripts

### logger

- Run from terminal at repo root: `./logger.py -w="Winner" -l="Looser" -s=<winner's sets>:<looser's sets>`.
- `-d` flag is optional (today is used by default). Day format is yyyy-mm-dd.
- `-b="<ball color>"` flag is used when play ball was red or blue. Yellow color is default.
- Also see `./logger.py --help`.

### get ratings

- Run from terminal at repo root: `./get_ratings.py`. This will update all json data for deployment.
- `-d` flag is optional, script will show ratings only if not current day specified. Day format is yyyy-mm-dd. 
- Also you can see `./get_ratings.py --help`.

### ui

- `npm run deploy` to update rating on [lzrby.github.io/squash](http://lzrby.github.io/squash)
