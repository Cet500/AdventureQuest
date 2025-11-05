import environ
import os

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


TG_API_KEY = env( 'TG_API_KEY' )
BASE_URL = env( 'BASE_URL', default = 'http://127.0.0.1:8000' )
