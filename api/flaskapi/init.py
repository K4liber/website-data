import os
import redis
from rq import Queue
from flask import Flask
import sqlalchemy

from flaskapi.config import config

# Flask init
api = Flask('api')
# SQLAlchemy init
db_engine = sqlalchemy.create_engine(
    f'mysql+mysqlconnector://'
    f'{config["db"]["user"]}:{config["db"]["password"]}'
    f'@{config["db"]["host"]}:{config["db"]["port"]}/'
    f'{config["db"]["name"]}')
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=db_engine)
# Redis init
listen = ['default']
redis_url = os.getenv('REDISTOGO_URL',
                      f'redis://{config["redis"]["host"]}:'
                      f'{config["redis"]["port"]}')
redis_conn = redis.from_url(redis_url)
redis_queue = Queue(connection=redis_conn)
