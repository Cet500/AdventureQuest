import environ
import os

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


VERSION = env( 'VERSION' )
DB_NAME = env( 'DB_NAME', default = 'database.db' )
