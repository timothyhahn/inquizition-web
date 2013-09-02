from inquizition import db
from datetime import datetime
import json


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    questions = db.Column(db.String(100))  # IDs stored as json
                                     # For example: {1, 2, 3, 4}
    responses = db.relationship('Response', backref='quiz')
    results = db.relationship('Result', backref='quiz')
    timers = db.relationship('Timer', backref='quiz')

    def __init__(self, name=None, start_time=None, end_time=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Quiz %r>' % (self.name)

    def info(self):
        quiz_dict = dict()
        quiz_dict['id'] = self.id
        quiz_dict['name'] = self.name
        quiz_dict['startTime'] = str(self.start_time)
        seconds_left = self.start_time - datetime.now()
        quiz_dict['secondsLeft'] = str(seconds_left.seconds)
        return quiz_dict

    def data(self):
        quiz_dict = self.info()

        question_id_list = json.loads(self.questions)
        questions_list = list()
        for question_id in question_id_list:
            question = Question.query.get(question_id)
            questions_list.append(question.data())
        quiz_dict['questions'] = questions_list

        return quiz_dict


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    responses = db.relationship('Response', backref='user')
    results = db.relationship('Result', backref='user')
    timers = db.relationship('Timer', backref='user')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<User %r>' % (self.name)

    def info(self):
        user_dict = dict()
        user_dict['id'] = self.id
        user_dict['name'] = self.name
        return user_dict


class Timer(db.Model):
    __tablename__ = 'timer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    last_answered = db.Column(db.DateTime)

    def __init(self, user_id=None, quiz_id=None, last_answered=None):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.last_answered = last_answered


class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_response = db.Column(db.Integer)
    time_elapsed = db.Column(db.Integer)

    def __init__(self, question_id=None, user_id=None, quiz_id=None, user_response=None):
        self.question_id = question_id
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.answered = False
        self.user_response = user_response
        self.time_elapsed = None

    def __repr__(self):
        return '<Response %d>' % (self.id)


class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id=None, quiz_id=None, score=None):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.score = score
        self.date = datetime.now()

    def __repr__(self):
        return '<Result %d>' % (self.id)

    def data(self):
        result_dict = dict()
        result_dict['id'] = self.id
        result_dict['score'] = self.score
        result_dict['quiz_id'] = self.quiz_id
        result_dict['user_id'] = self.user_id
        result_dict['username'] = User.query.get(self.user_id).name
        result_dict['date'] = self.date
        result_dict['quizname'] = Quiz.query.get(self.quiz_id).name

        return result_dict


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    correct_answer_id = db.Column(db.Integer)
    responses = db.relationship('Response', backref='question')
    answers = db.relationship('Answer', backref='question')

    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return '<Question %r>' % (self.text)

    def data(self):
        question = dict()
        answer_list = list()
        for answer in Answer.query.filter(Answer.question_id == self.id):
            answer_dict = dict()
            answer_dict['id'] = answer.id
            answer_dict['text'] = answer.text
            answer_list.append(answer_dict)

        question['text'] = self.text
        question['id'] = self.id
        question['answers'] = answer_list
        return question


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __init__(self, text=None, question_id=None):
        self.text = text
        self.question_id = question_id

    def data(self):
        answer = dict()
        answer['id'] = self.id
        answer['text'] = self.text
        return answer
