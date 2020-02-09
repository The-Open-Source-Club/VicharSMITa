from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__,
            static_url_path='',
            static_folder='www/static',
            template_folder='www')
db = SQLAlchemy()
migrate = Migrate(app, db)
login = LoginManager(app)
app.config.from_object(Config)

from app import routes, datamodel
