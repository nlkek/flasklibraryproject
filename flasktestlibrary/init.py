from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask_bootstrap import Bootstrap

app = Flask('__main__')
app.config.from_object('config')
dbs = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
import views, models

