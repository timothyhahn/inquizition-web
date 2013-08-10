from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask import jsonify
from database import Base, db_session
import json


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    last_answered = Column(DateTime)

    questions = Column(String(100)) ## IDs stored as json
                                    ## For example: {1, 2, 3, 4}
    responses = relationship('Response', backref='quiz')
    results = relationship('Result', backref='quiz')
    
    def __init__(self, name=None, start_time=None, end_time=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Quiz %r>' % (self.name)

    def info(self):
        quiz_dict = dict()
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
        

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    responses = relationship('Response', backref='user')
    results = relationship('Result', backref='user')

    
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<User %r>' % (self.name)

class Response(Base):
    __tablename__ = 'response'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    user_response = Column(Integer)
    time_elapsed = Column(Integer)

    def __init__(self, question_id=None, user_id=None, quiz_id=None, user_response=None):
        self.question_id = question_id
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.answered = False
        self.user_response = user_response
        self.time_elapsed = None
        
    def __repr__(self):
        return '<Response %d>' % (self.id)

class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    score = Column(Integer)
    date = Column(DateTime, nullable=False)

    def __init__(self, user_id, quiz_id, score=None):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.score = score
        self.date = datetime.datetime.now
        
    def __repr__(self):
        return '<Result %d>' % (self.id)


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    text = Column(String(120), nullable=False)
    correct_answer_id = Column(Integer)
    responses = relationship('Response', backref='question')
    answers = relationship('Answer', backref='question')

    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return '<Question %r>' % (self.text)

    def data(self):
        question = dict()
        answer_list = list()
        for answer in Answer.query.filter(Answer.question_id == self.id):
            answer_dict = dict()
            answer_dict['answerID'] = answer.id
            answer_dict['answerText'] = answer.text
            answer_list.append(answer_dict)

        question['questionText'] = self.text
        question['questionID'] = self.id
        question['answers'] = answer_list
        return question

class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    text = Column(String(120), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)

    def __init__(self,text=None, question_id = None):
        self.text = text
        self.question_id = question_id
    
    def data(self):
        answer['answerID'] = self.id
        answer['text'] = self.text
        return answer

