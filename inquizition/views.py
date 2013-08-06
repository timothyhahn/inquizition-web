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

    if quiz:
        json = quiz.json()
    else:
        json = '{}'
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
    else:
        json = '{}'

    return json

@app.route('/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    ## Get question
    question = Question.query.filter(Question.id == question_id).first()
    if question:
        json = question.json()
    else:
        json = '{}'

    ## Convert to json
    return json

@app.route('/question', methods=['GET'])
def get_random_question():
    ## Get random question
    query = db_session.query(Question)
    rowCount = int(query.count())
    question = query.offset(int(rowCount*random.random())).first()

    if question:
        json = question.json()
    else:
        json = '{}'

    ## Convert to JSON
    return json

## POST
@app.route('/quiz/<int:quiz_id>', methods=['POST'])
def answer_quiz(quiz_id):
    ## Get user from request
    user = User.query.filter(User.id == (str)request.form['user_id']).first()

    ## Get question from request
    question = User.query.filter(Question.id == (str).request.form['question_id'])
    ## Get answer from request
    answer = (str) request.form['answer']
    ## Answer quiz
    quiz = Quiz.query.filter(Quiz.id == quiz_id).first()
    ## Store response
    response = Response.query.filter(Response.quiz_id == quiz_id).filter(Response.user_id == user.id).filter(Response.question_id == question.id)

    response.user_response = answer

    now = datetime.now()
    then = quiz.last_answered

    response.time_elapsed = now - then
    quiz.last_answered = datetime.now()

    result_dict = dict()
    ## Find out if that response is correct
    if(response.user_response == response.correct_response):
        result_dict['correct'] = "True"
    else:
        result_dict['correct'] = "False"

    json = json.dumps(result_dict)
    db_session.commit()
    return json

@app.route('/quiz/create/', methods=['POST'])
def create_quiz():
    ## Create quiz
    quiz_name = (str)(request.form['quiz_name'])
    quiz = Quiz(name=quiz_name)
    ## Pick questions for that quiz
    question_list = list()
    for index in range(0,10):
        ## pick random question
        qid = 1
        question_list.append(qid)

    quiz.questions = json.dumps(question_list)

    start_time = datetime.now() + datetime.timedelta(minutes=1)
    end_time = start_time + datetime.timedelta(minutes=10)

    db_session.add(quiz)
    db_session.commit()
    ## Join creator to quiz
    return redirect(url_for('join_quiz'),quiz_id=quiz.id))

@app.route('/quiz/join/<int:quiz_id>', methods=['POST'])
def join_quiz(quiz_id):
    ## Get user from request
    user = User.query.filter(User.id == request.form['user_id']).first()
    ## Create responses for user
    for index in range(0,10):
        print "TODO"
        response = Response(question_id=qid, user_id=user.id, quiz_id=quiz.id)
        response.correct_response="TODO"
        db_session.add(response)

    ## Store responses for user
    db_session.commit()
    print ""

## TODO
## * Login
## * Register


# TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

