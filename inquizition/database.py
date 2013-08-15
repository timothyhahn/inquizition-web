from inquizition import db
## Start DB
def init_db():
#    import models
    db.create_all()


def clear_db():
    db.drop_all()


def purge_db():
    from models import Quiz, Response
    from datetime import datetime
    quizzes = Quiz.query.filter(Quiz.end_time < datetime.now())
    for quiz in quizzes:
        responses = Response.query.filter(Response.quiz_id == quiz.id)
        for response in responses:
            db.session.delete(response)
        db.session.delete(quiz)
    db.session.commit()
