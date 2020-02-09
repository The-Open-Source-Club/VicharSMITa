from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
			static_url_path='', 
            static_folder='www/static',
            template_folder='www')
db = SQLAlchemy();
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
from app import routes, datamodel
