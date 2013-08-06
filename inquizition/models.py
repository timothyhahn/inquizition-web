from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask import jsonify
from database import Base
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
    
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Quiz %r>' % (self.name)

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
    answered = Column(Boolean)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    user_response = Column(String(1))
    correct_response = Column(String(1),nullable=False)
    time_elapsed = Column(DateTime)

    def __init__(self, question_id=None, user_id=None, quiz_id=None):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.answered = False
        
    def __repr__(self):
        return '<Response %d>' % (self.id)

class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    score = Column(Integer)
    date = Column(DateTime, nullable=False)

    def __init__(self, user_id, quiz_id, score):
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
    correct_answer = Column(String(120))
    other_answer1 = Column(String(120))
    other_answer2 = Column(String(120))
    other_answer3 = Column(String(120))
    responses = relationship('Response', backref='question')

    def __init__(self, text=None, correct_answer=None, other_answer1=None, other_answer2=None, other_answer3=None):
        self.text = text
        self.correct_answer = correct_answer
        self.other_answer1 = other_answer1
        self.other_answer2 = other_answer2
        self.other_answer3 = other_answer3

    def __repr__(self):
        return '<Question %r>' % (self.text)

    def json(self):
        question = dict()
        answers = [self.correct_answer, self.other_answer1, self.other_answer2, self.other_answer3]

        question['questionText'] = self.text
        question['questionID'] = self.id
        question['answers'] = answers
        return jsonify(question)
