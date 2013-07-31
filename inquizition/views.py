from inquizition import app
from flask import url_for, redirect, request, render_template, session, flash
from forms import LoginForm, RegisterForm
from database import db_session
from models import Quiz

## HOW TO SIMPLY SHOW A STATIC PAGE
@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))


## SIMPLE ROUTE
@app.route('/hello')
def hello_world():
    return 'Hello World!'


## DB QUERY + TEMPLATE
@app.route('/quiz', methods=['GET'])
def list_quiz():
    quizzes = Quiz.query.all()
    return render_template('show_entries.html', quizzes=quizzes)

@app.route('/quiz/json', methods=['GET'])
def list_quiz_json():
    json = "{"
    quizzes = Quiz.query.all()
    for quiz in quizzes:
        json += '"quiz": '
        json += '"' + quiz.name +'",'
    json += "}"
    return json


## HOW TO "RECEIVE" DATA AND DB TRANSACTION
@app.route('/quiz/create', methods=['POST'])
def create_quiz():
    quizName = (str)(request.form['qname'])
    q = Quiz(quizName)
    db_session.add(q)
    db_session.commit()    
    print quizName
    return '{"status": "OK", "quiz name": "'+quizName+'"}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        lForm = LoginForm(request.form, prefix='lForm')
        if lForm.validate():
            return redirect('/hello')
        else:
            flash('what')
            rForm = RegisterForm(prefix='rForm')
            return render_template('login.html', lForm=lForm, rForm=rForm)

    if request.method == 'GET':
        lForm = LoginForm(prefix='lForm')
        rForm = RegisterForm(prefix='rForm')
        return render_template('login.html', lForm=lForm, rForm=rForm)

@app.route('/register', methods=['POST'])
def register():
    rForm = RegisterForm(request.form, prefix='rForm')

    if rForm.validate():
        return redirect('/hello')
    else:
        lForm = RegisterForm(prefix='lForm')
        return render_template('login.html', lForm=lForm, rForm=rForm)


## TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



