from inquizition import app
from flask import url_for, redirect, request, render_template, session, flash
from database import db_session
from models import Quiz

# Homepage
@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))


# API
## GET
@app.route('/quiz', methods=['GET'])
def list_quizzes():
    ## List all quizzes
    ## Convert to json
    return json

@app.route('/quiz/<int:quiz_id>',methods['GET'])
def find_quiz(quiz_id):
    ## Find quiz at id
    ## Convert to json
    return json

@app.route('/quiz/results/<int:quiz_id>',methods['GET'])
def quiz_results(quiz_id):
    ## Find results for quiz
    ## Order them by score
    ## Convert to json
    return json

@app.route('/user/<int:user_id>', methods['GET'])
def user_results(user_id):
    ## Get Username
    ## Get list of user results
    ## Order them by date
    ## Convert to json
    return json

@app.route('/question/<int:question_id>', methods['GET'])
def get_question(question_id):
    ## Get question
    ## Convert to json
    return json

@app.route('/question', methods['GET'])
def get_random_question():
    ## Get random question
    ## Convert to json

## POST
@app.route('/quiz/<int:quiz_id>', methods['POST'])
def answer_quiz(quiz_id):
    ## Get user name from request
    ## Get answer from request
    ## Find the next question to be answered
    ## Answer quiz
    ## Store response
    ## Find out if that response is correct
    return json

@app.route('/quiz/create/', methods['POST'])
def create_quiz():
    ## Create quiz
    ## Pick questions for that quiz
    ## Join creator to quiz id
    return json

@app.route('/quiz/join/<int:quiz_id>', methods['POST'])
def join_quiz(quiz_id):
    ## Get user from request
    ## Create responses for user
    ## Store responses for user
    print ""


# TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

