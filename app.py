from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager
from flask_avatars import Avatars
import os

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
avatars = Avatars(app)

basedir = os.path.abspath(os.path.dirname(__name__))

app.config['AVATARS_SAVE_PATH'] = os.path.join(basedir, 'avatars')
