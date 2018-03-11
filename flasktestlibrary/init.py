from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from config import basedir

app = Flask('__main__')
app.config.from_object('config')
dbs = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
import views, models

