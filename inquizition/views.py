from inquizition import app, db
from flask import url_for, redirect, request, jsonify
from models import Quiz, Result, User, Question, Answer, Response
from datetime import datetime, timedelta
from helpers import generate_results
import json
import random


@app.route('/')  # Homepage
def home():
    return redirect(url_for('static', filename='index.html'))

# API
## GET


@app.route('/quiz', methods=['GET'])
def get_quizzes():
    ## List all quizzes that are available
    quizzes = Quiz.query.filter(Quiz.start_time > datetime.now())

    ## Convert to json
    if quizzes.count() > 0:
        quizzes_dict = dict()
        quizzes_dict['quizzes'] = list()

        for quiz in quizzes:
            quizzes_dict['quizzes'].append(quiz.info())
            json_results = jsonify(quizzes_dict)

    else:
        json_results = jsonify(dict())
    return json_results


@app.route('/name')
def get_random_name():
    f = open('wordlist', 'r')
    words = []
    for line in f:
        words.append(line.strip('\n'))
    f.close()

    word1 = str(words[random.randint(0, len(words) - 1)]).capitalize()
    word2 = str(words[random.randint(0, len(words) - 1)]).capitalize()
    return '%s %s' % (word1, word2)


@app.route('/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    ## Find quiz at idone.drexel.edu
    quiz = Quiz.query.get(quiz_id)

    ## TODO: Check that you can only download maybe 10 seconds before it starts
    if quiz:
        json_results = jsonify(quiz.data())
    else:
        json_results = jsonify(dict())
    ## Convert to json
    return json_results


@app.route('/quiz/seconds/<int:quiz_id>')
def get_seconds(quiz_id):
    quiz = Quiz.query.get(quiz_id)

    if quiz:
        results = str((quiz.start_time - datetime.now()).seconds)
    else:
        results = ""

    return results


@app.route('/quiz/joiners/<int:quiz_id>', methods=['GET'])
def get_quiz_joiners(quiz_id):
    responses = Response.query.filter(Response.quiz_id == quiz_id)
    user_set = set()
    for response in responses:
        user_set.add(response.user_id)

    user_list = list(user_set)
    joiner_list = list()
    for user_id in user_list:
        user_dict = dict()
        user = User.query.get(user_id)

        user_dict['id'] = user.id
        user_dict['name'] = user.name
        joiner_list.append(user_dict)
    joiner_dict = dict()
    joiner_dict['joiners'] = joiner_list
    return jsonify(joiner_dict)


@app.route('/quiz/results/<int:quiz_id>', methods=['GET'])
def get_quiz_results(quiz_id):
    ## Find results for quiz and order them by score
    generate_results(quiz_id)
    results = Result.query.filter(Result.quiz_id == quiz_id).order_by(Result.score.desc())

    ## Convert to json
    if results.count() > 0:
        results_dict = dict()
        results_dict['results'] = list()

        for result in results:
            results_dict['results'].append(result.data())

        json_results = jsonify(results_dict)
    else:
        json_results = jsonify(dict())

    return json_results


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_results(user_id):
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
                results_list.append(result.data())

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
        json_results = jsonify(question.data())
    else:
        json_results = jsonify(dict())

    ## Convert to json
    return json_results


@app.route('/question', methods=['GET'])
def get_random_question():
    ## Get random question
    query = db.session.query(Question)
    rowCount = int(query.count())
    question = query.offset(int(rowCount*random.random())).first()

    if question:
        json_results = jsonify(question.data())
    else:
        json_results = jsonify(dict())

    ## Convert to JSON
    return json_results

## POST


@app.route('/quiz/answer/<int:quiz_id>', methods=['POST'])
def answer_quiz(quiz_id):
    ## TODO: Error handling if they try to answer the same question twice
    ## Get user from request
    user_id = (int)(request.form['user_id'])
    ## Get question from request
    question = Question.query.get((int)(request.form['question_id']))
    question_id = request.form['question_id']
    ## Get answer from request
    answer = (int)(request.form['answer'])
    ## Answer quiz
    quiz = Quiz.query.get(quiz_id)
    ## Store response
    response = Response.query.filter(Response.quiz_id == quiz_id).filter(Response.user_id == user_id).filter(Response.question_id == question_id).first()

    response.user_response = answer

    now = datetime.now()
    then = quiz.last_answered

    time_elapsed = now - then
    seconds = int(time_elapsed.seconds)
    if(time_elapsed.microseconds > 50000):
        seconds += 1

    response.time_elapsed = seconds
    quiz.last_answered = datetime.now()
    db.session.commit()

    generate_results(quiz_id)
    result = Result.query.filter(Result.quiz_id == quiz_id).filter(Result.user_id == user_id).first()

    result_dict = dict()
    ## Find out if that response is correct
    correct_answer = Answer.query.get(question.correct_answer_id)
    if(answer == correct_answer.id):
        result_dict['correct'] = 'True'
        result_dict['text'] = ''
        result_dict['score'] = result.score
    else:
        result_dict['correct'] = 'False'
        result_dict['text'] = correct_answer.text
        result_dict['score'] = result.score

    json_results = jsonify(result_dict)
    db.session.commit()
    return json_results


@app.route('/quiz/create', methods=['GET', 'POST'])
def create_quiz():

    ## Create quiz
    quiz_name = (str)(request.form['quiz_name'])
    #quiz_name = "HELLO VIETNAM"
    quiz = Quiz(name=quiz_name)
    ## Pick questions for that quiz
    question_list = list()
    question_count = db.session.query(Question).count()

    for _ in range(0, 10):
        searching = True
        while searching:
            number = random.randint(1, question_count - 1)
            if number not in question_list:
                question_list.append(number)
                searching = False

    quiz.questions = json.dumps(question_list)

    seconds_later = 60

    if 'seconds' in request.form.keys():
        seconds_later = (int)(request.form['seconds'])
    quiz.start_time = datetime.now() + timedelta(seconds=seconds_later)
    quiz.end_time = quiz.start_time + timedelta(minutes=10)
    quiz.last_answered = quiz.start_time

    db.session.add(quiz)
    db.session.commit()

    status_dict = dict()
    status_dict['status'] = 'CREATED'
    return jsonify(status_dict)


@app.route('/quiz/join/<int:quiz_id>', methods=['GET', 'POST'])
def join_quiz(quiz_id, user_id=None):
    ## TODO: Only allow joining once
    ## Get user from request
    if request:
        user = User.query.get(request.form['user_id'])
    else:
        user = User.query.get(user_id)
    quiz = Quiz.query.get(quiz_id)
    ## Create responses for user
    for index in range(0, 10):
        questions = json.loads(quiz.questions)
        response = Response(question_id=questions[index], user_id=user.id, quiz_id=quiz_id)
        response.correct_response = "A"
        db.session.add(response)

    ## Store responses for user
    db.session.commit()
    return "JOINED"


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    user = User.query.filter(User.name == username).first()
    if not user:
        user = User(name=username)
        db.session.add(user)
        db.session.commit()
    return jsonify(user.info())


# TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
