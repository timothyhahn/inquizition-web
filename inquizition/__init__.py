from flask import Flask
from settings import debug

app = Flask(__name__,static_url_path="/app", static_folder="app")

if debug:
    from flask.ext.admin import Admin
    from flask.ext.admin.contrib.sqlamodel import ModelView
    from models import User, Quiz, Question, Response, Result
    from database import db_session
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    admin = Admin(app)
    admin.add_view(ModelView(User, db_session))
    admin.add_view(ModelView(Quiz, db_session))
    admin.add_view(ModelView(Question, db_session))
    admin.add_view(ModelView(Response, db_session))
    admin.add_view(ModelView(Result, db_session))


import inquizition.views
