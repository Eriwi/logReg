from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'index'
app.config.from_object(Config)
db = SQLAlchemy(app)



from server import routes, models

