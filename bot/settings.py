import os

from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TG_TOKEN')
groups = [-325409771]
admins = ['drapegnik', 'klicunou']

GAME_FORMAT = '/game @Drapegnik 5:0 @uladbohdan'
REPO_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
