from inquizition import app
from flask import url_for, redirect, request, render_template, session, flash,jsonify
from database import db_session
from models import Quiz, Result, User, Question, Answer, Response
from datetime import datetime, timedelta
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
    if quizzes.count() > 0:
        quizzes_dict = dict()
        quizzes_dict['quizzes'] = list()

        for quiz in quizzes:
            quizzes_dict['quizzes'].append(json.loads(quiz.info()))
            json_results = jsonify(quizzes_dict)
    else: 
        json_results = jsonify(dict())
    return json_results

@app.route('/quiz/<int:quiz_id>',methods=['GET'])
def find_quiz(quiz_id):
    ## Find quiz at id
    quiz = Quiz.query.get(quiz_id)

    if quiz:
        json_results = quiz.json()
    else:
        json_results = jsonify(dict())
    ## Convert to json
    return json_results

@app.route('/quiz/results/<int:quiz_id>',methods=['GET'])
def quiz_results(quiz_id):
    ## Find results for quiz and order them by score
    results = Result.query.filter(Result.quiz_id == quiz_id).order_by(Result.score.desc())

    ## Convert to json
    if results.count() > 0:
        results_dict = dict()
        results_dict['results'] = list()

        for result in results:
            results_dict['results'].append(json.loads(result.json()))

        json_results = json.jsonify(results_dict)
    else:
        json_results = jsonify(dict())

    return json_results

@app.route('/user/<int:user_id>', methods=['GET'])
def user_results(user_id):
    ## Get User
    user = User.query.get(user_id)

    if user:
        user_dict = dict()
        ## Get Username
        user_dict['name'] = user.name

        ## Get list of user results
        results = Result.query.filter(Result.user_id == user_id).order_by(Result.date)
        if results.count() > 0:
            results_list = list()

            ## Add results to a list
            for result in results:
                results_list.append(json.loads(result.json()))

            ## Add results list to user dictionary that wil be dumped to JSON
            user_dict['results'] = results_list
        else:
            user_dict = list()

        json_results = jsonify(user_dict)
    else:
        json_results = jsonify(dict())

    return json_results

@app.route('/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    ## Get question
    question = Question.query.get(question_id)
    if question:
        json_results = question.json()
    else:
        json_results = jsonify(dict())

    ## Convert to json
    return json_results

@app.route('/question', methods=['GET'])
def get_random_question():
    ## Get random question
    query = db_session.query(Question)
    rowCount = int(query.count())
    question = query.offset(int(rowCount*random.random())).first()

    if question:
        json_results = question.json()
    else:
        json_results = jsonify(dict())

    ## Convert to JSON
    return json_results

## POST
@app.route('/quiz/answer/<int:quiz_id>', methods=['POST'])
def answer_quiz(quiz_id):
    ## Get user from request
    user = User.query.get((int)(request.form['user_id']))

    ## Get question from request
    question = Question.query.get((int)(request.form['question_id']))
    question_id = request.form['question_id']
    ## Get answer from request
    answer = (int)(request.form['answer'])
    ## Answer quiz
    quiz = Quiz.query.get(quiz_id)
    ## Store response
    response = Response.query.filter(Response.quiz_id == quiz_id).filter(Response.user_id == user.id).filter(Response.question_id == question_id).first()

    response.user_response = answer

    now = datetime.now()
    then = quiz.last_answered

    time_elapsed = now - then
    response.time_elapsed = int(time_elapsed.seconds)
    quiz.last_answered = datetime.now()

    result_dict = dict()
    ## Find out if that response is correct
    correct_answer = Answer.query.get(question.correct_answer_id)
    print answer
    print correct_answer.id
    if(answer == correct_answer.id):
        result_dict['correct'] = 'True'
    else:
        result_dict['correct'] = 'False'

    json_results = jsonify(result_dict)
    db_session.add(response)
    db_session.commit()
    return json_results

@app.route('/quiz/create', methods=['GET','POST'])
def create_quiz():
    ## Create quiz
    quiz_name = (str)(request.form['quiz_name'])
    #quiz_name = "HELLO VIETNAM"
    quiz = Quiz(name=quiz_name)
    ## Pick questions for that quiz
    question_list = list()
    #for index in range(0,10):
        ## pick random question
   #     qid = 1
   #     question_list.append(qid)
    question_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    quiz.questions = json.dumps(question_list)

    quiz.start_time = datetime.now() + timedelta(minutes=1)
    print quiz.start_time
    quiz.end_time = quiz.start_time + timedelta(minutes=10)
    print quiz.end_time
    quiz.last_answered = quiz.start_time

    db_session.add(quiz)
    db_session.commit()
    ## Join creator to quiz
    return join_quiz(quiz.id, request.form['user_id'])
    #return redirect(url_for('join_quiz'),quiz_id=quiz.id)

@app.route('/quiz/join/<int:quiz_id>', methods=['GET','POST'])
def join_quiz(quiz_id, user_id=None):
    ## Get user from request
    if request:
        user = User.query.get(request.form['user_id'])
    else:
        user = User.query.get(user_id)
    ## Create responses for user
    for index in range(0,10):
        print "TODO"
        response = Response(question_id=index, user_id=user.id, quiz_id=quiz_id)
        response.correct_response="A"
        db_session.add(response)

    ## Store responses for user
    db_session.commit()
    return "MADE AND JOINED"

@app.route('/login', methods=['POST'])
def login():
    return "HI"

@app.route('/register', methods=['POST'])
def register():
    return "BI"


# TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

