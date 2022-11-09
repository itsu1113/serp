import os
from os.path import join, dirname
from dotenv import load_dotenv
accesskey = '' # enter real access key here

env_file = dirname(__file__) + '/.env'
load_dotenv(env_file)

db_config = {
    'mysql': {
        'driver': 'mysql',
        'host': os.environ.get("DB_HOST"),
        'database': os.environ.get("DB_DATABASE"),
        'user': os.environ.get("DB_USERNAME"),
        'password': os.environ.get("DB_PASSWORD"),
        'prefix': ''
    }
}
