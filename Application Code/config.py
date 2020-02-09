import os
import random
import time
basedir = os.path.abspath(os.path.dirname(__file__))
random.seed(time.time)

class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(random.random())
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
