from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Quiz %r>' % (self.name)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80))

class Responses(Base):
    __tablename__ = 'response'
    id = Column(Integer, primary_key=True)
    answered = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.id'))
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    user_response = Column(String(1))
    correct_response = Column(String(1))
    time_elapsed = Column(DateTime)

class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    score = Column(Integer)

class Questions(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    correct_answer = Column(String(120))
    other_answer1 = Column(String(120))
    other_answer2 = Column(String(120))
    other_answer3 = Column(String(120))

