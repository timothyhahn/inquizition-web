from database import db_session
from models import Question, Answer
import random

def gen_math():
    operation = random.randint(0,2) # 0 add 1 sub 2 mult
    if operation > 1:
        first_num = random.randint(1,15)
        second_num = random.randint(1,15)
    else:
        first_num = random.randint(1,40)
        second_num = random.randint(1,40)
    if operation is 0:
        question = "What is %d + %d" % (first_num, second_num)
        correct_answer = first_num + second_num
        other_answer1 = first_num * second_num
        other_answer2 = first_num - second_num
        other_answer3 = (first_num - random.randint(1,2)) + second_num
    elif operation is 1:
        question = "What is %d - %d" % (first_num, second_num)
        correct_answer = first_num - second_num
        other_answer1 = first_num - (random.randint(1,4) + second_num)
        other_answer2 = first_num + second_num
        other_answer3 = (first_num - random.randint(3,5)) - second_num
    else:
        question = "What is %d * %d" % (first_num, second_num)
        correct_answer = first_num * second_num
        other_answer1 = first_num * (random.randint(2,3) +second_num)
        other_answer2 = first_num + second_num
        other_answer3 = (first_num + random.randint(1,2)) * second_num

    q = Question(text=question)
    db_session.add(q)
    db_session.flush()
    db_session.refresh(q)

    ca = Answer(text=str(correct_answer), question_id=q.id)
    oa1= Answer(text=str(other_answer1), question_id=q.id)
    oa2= Answer(text=str(other_answer2), question_id=q.id)
    oa3= Answer(text=str(other_answer3), question_id=q.id)

    answers = [ca, oa1, oa2, oa3]
    random.shuffle(answers)

    for a in answers:
        db_session.add(a)

    db_session.flush()
    db_session.refresh(ca)
    q.correct_answer_id = ca.id
    db_session.add(q)
    db_session.commit()

def gen_dummy_data():
    for _ in range(1, 100):
        gen_math()
