from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
import json


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    questions = Column(String(100)) ## IDs stored as json
                                    ## For example: {1, 2, 3, 4}
    
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Quiz %r>' % (self.name)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    
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

    def __init__(self, question_id, user_id, quiz_id):
        this.user_id = user_id
        this.quiz_id = quiz_id
        this.answered = False
        
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
        this.user_id = user_id
        this.quiz_id = quiz_id
        this.score = score
        this.date = datetime.datetime.now
        
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

    def __init__(self, text):
        this.text = text
        
    def __repr__(self):
        return '<Question %r>' % (self.text)

    def json(self):
        question = dict()
        answers = [correct_answer, other_answer1, other_answer2, other_answer3]

        question['questionText'] = text
        question['questionID'] = id
        question['answers'] = answers
        return json.dumps(question)
