from inquizition import app
from flask import url_for, redirect, request, render_template, session, flash
from database import db_session
from models import Quiz

## Homepage
@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))


## API
@app.route('/quiz', methods=['GET'])
def list_quiz_json():
    return json


## TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



