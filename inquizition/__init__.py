from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from settings import debug, database_path
import os


app = Flask(__name__, static_url_path="/app", static_folder="app")

if os.environ.get('TESTING') != 'true':
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path

db = SQLAlchemy(app)


if debug:
    from flask.ext.admin import Admin
    from flask.ext.admin.contrib.sqlamodel import ModelView
    from models import User, Quiz, Question, Response, Result, Answer
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Quiz, db.session))
    admin.add_view(ModelView(Question, db.session))
    admin.add_view(ModelView(Response, db.session))
    admin.add_view(ModelView(Result, db.session))
    admin.add_view(ModelView(Answer, db.session))


import inquizition.views
