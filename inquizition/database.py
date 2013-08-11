from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import database_path

## Create database
engine = create_engine(database_path, convert_unicode=True)
## Default database session
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

## Base class for all models
Base = declarative_base()
Base.query = db_session.query_property()


## Start DB
def init_db():
    ## Import models
    import models
    Base.metadata.create_all(bind=engine)
    ## TODO
    ## Import questions

def clear_db():
    Base.metadata.drop_all(engine)

def purge_db():
    from models import Quiz, Response
    from datetime import datetime
    quizzes = Quiz.query.filter(Quiz.end_time < datetime.now())
    for quiz in quizzes:
        responses = Response.query.filter(Response.quiz_id == quiz.id)
        for response in responses:
            db_session.delete(response)
        db_session.delete(quiz)
    db_session.commit()
