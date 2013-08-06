from inquizition import app
from flask import url_for, redirect, request, render_template, session, flash
from database import db_session
from models import Quiz, Result, User, Question
from datetime import datetime
import json, random

# Homepage
@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))


# API
## GET
@app.route('/quiz', methods=['GET'])
def list_quizzes():
    ## List all quizzes that are available
    quizzes = Quiz.query.filter(Quiz.start_time > datetime.now())


    ## Convert to json
    if len(quizzes) > 0:
        quizzes_dict = dict()
        quizzes_dict['quizzes'] = list()

        for quiz in quizzes:
            quizzes_dict['quizzes'].append(json.loads(quiz.json()))

            json = json.dumps(quizzes_dict)
    else:
        json = '{}'
    return json

@app.route('/quiz/<int:quiz_id>',methods=['GET'])
def find_quiz(quiz_id):
    ## Find quiz at id
    quiz = Quiz.query.filter(Quiz.id = quiz_id).first()
    if quiz is None:
        json = '{}'
    else:
        json = quiz.json()
    ## Convert to json
    return json

@app.route('/quiz/results/<int:quiz_id>',methods=['GET'])
def quiz_results(quiz_id):
    ## Find results for quiz and order them by score
    results = Result.query.filter(Result.quiz_id == quiz_id).order_by(Result.score.desc())

    ## Convert to json
    if len(results) > 0:
        results_dict = dict()
        results_dict['results'] = list()

        for result in results:
            results_dict['results'].append(json.loads(result.json()))

        json = json.dumps(results_dict)
    else:
        json = '{}'

    return json

@app.route('/user/<int:user_id>', methods=['GET'])
def user_results(user_id):
    ## Get User
    user = User.query.filter(User.id == user_id).first()

    if user is None:
        json = '{}'
    else:
        user_dict = dict()
        ## Get Username
        user_dict['name'] = user.name

        ## Get list of user results
        results = Result.query.filter(Result.user_id == user_id).order_by(Result.date)
        if len(results) > 0:
            results_list = list()

            ## Add results to a list
            for result in results:
                results_list.append(json.loads(result.json()))

            ## Add results list to user dictionary that wil be dumped to JSON
            user_dict['results'] = results_list
        else:
            user_dict = list()

        json = json.dumps(user_dict)

    return json

@app.route('/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    ## Get question
    question = Question.query.filter(Question.id == question_id).first()
    if question is None:
        json = '{}'
    else:
        json = question.json()

    ## Convert to json
    return json

@app.route('/question', methods=['GET'])
def get_random_question():
    ## Get random question
    query = db_session.query(Question)
    rowCount = int(query.count())
    question = query.offset(int(rowCount*random.random())).first()

    if question is None:
        json = '{}'
    else:
        json = question.json()

    ## Convert to JSON
    return json

## POST
@app.route('/quiz/<int:quiz_id>', methods=['POST'])
def answer_quiz(quiz_id):
    ## Get user name from request
    ## Get answer from request
    ## Find the next question to be answered
    ## Answer quiz
    ## Store response
    ## Find out if that response is correct
    return json

@app.route('/quiz/create/', methods=['POST'])
def create_quiz():
    ## Create quiz
    ## Pick questions for that quiz
    ## Join creator to quiz id
    return json

@app.route('/quiz/join/<int:quiz_id>', methods=['POST'])
def join_quiz(quiz_id):
    ## Get user from request
    ## Create responses for user
    ## Store responses for user
    print ""

## TODO

## * Login
## * Register


# TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

