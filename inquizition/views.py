
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


## TURN OFF DB
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



