import os

from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TG_TOKEN')
groups = [-325409771, -303486770]
admins = []
active_tournaments = {'LZR Open': 'group stage'}


REPO_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA_DIR = os.path.abspath(os.path.join(REPO_ROOT_DIR, 'data/'))
