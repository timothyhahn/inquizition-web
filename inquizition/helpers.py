from database import db_session
from models import Question, Answer, Result, Response
import random,csv

def load_questions():
    questions = list()
    with open('trivia.csv', 'rb') as triviafile:
        reader = csv.reader(triviafile, delimiter=',')
        for row in reader:
    
            question = dict()
            # Ensure Length
            if len(row) != 6:
                print "ERROR: Wrong number of fields"
                print row
                break
    
            question['question'] = row[0]
            question['answers'] = row[1:5]
            question['correct_answer'] = row[5]
            
            # Ensure correctness
            if question['correct_answer'] not in question['answers']:
                print "ERROR: Correct answer not one of given answers"
                print "ERROR: Correct answer is '%s'" % (question['correct_answer'])
                for a in question['answers']:
                    print "ERROR: Possible answer is '%s'" % (a)
    
            answer_set = set(question['answers'])
            correct_set = set((question['correct_answer'],))
            question['answers'] = list(answer_set - correct_set)
    
            # Ensure removedness
            if len(question['answers']) != 3:
                print "ERROR: Correct still in answer"
                print "ERROR: Correct answer is '%s'" % (question['correct_answer'])
                for a in question['answers']:
                    print "ERROR: Possible answer is '%s'" % (a)
    
            questions.append(question)
            print question

    for question in questions:
        q = Question(text=question['question'])
        db_session.add(q)
        db_session.flush()
        db_session.refresh(q)

        ca = Answer(text=str(question['correct_answer']), question_id=q.id)
        oa1= Answer(text=str(question['answers'][0]), question_id=q.id)
        oa2= Answer(text=str(question['answers'][1]), question_id=q.id)
        oa3= Answer(text=str(question['answers'][2]), question_id=q.id)

        answers = [ca, oa1, oa2, oa3]
        random.shuffle(answers)

        for a in answers:
            db_session.add(a)

        db_session.flush()
        db_session.refresh(ca)
        q.correct_answer_id = ca.id
        db_session.add(q)
    db_session.commit()


def generate_results(quiz_id):
    # Find all users who have responses
    responses = Response.query.filter(Response.quiz_id == quiz_id)
    user_set = set()
    for response in responses:
        user_set.add(response.user_id)

    user_list = list(user_set)
        
    scores_dict = dict()
    # For each user calculate result
    for user_id in user_list:
        score = 0
        responses = Response.query.filter(Response.quiz_id == quiz_id).filter(Response.user_id == user_id)
        for response in responses:
            ## Get if correct
            question = Question.query.get(response.question_id)
            if response.time_elapsed is not None:
                if response.user_response == question.correct_answer_id:
                    ## Get how long it took
                    score += 60 - response.time_elapsed
                else:
                    score -= 10
        scores_dict[user_id] = score

    for user_id in scores_dict.keys():
        ## Find old result if it exists
        result = Result.query.filter(Result.user_id == user_id).filter(Result.quiz_id == quiz_id).first()
        if result:
            result.score = scores_dict[user_id]
        else:
            result = Result(user_id = user_id, quiz_id = quiz_id, score = scores_dict[user_id])
        db_session.add(result)
        
    db_session.commit()




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
        other_answer3 = (first_num - random.randint(2,4)) + second_num
    elif operation is 1:
        question = "What is %d - %d" % (first_num, second_num)
        correct_answer = first_num - second_num
        other_answer1 = first_num - (random.randint(2,5) + second_num)
        other_answer2 = first_num + second_num
        other_answer3 = (first_num - random.randint(3,6)) - second_num
    else:
        question = "What is %d * %d" % (first_num, second_num)
        correct_answer = first_num * second_num
        other_answer1 = first_num * (random.randint(2,3) + second_num)
        other_answer2 = first_num + second_num
        other_answer3 = (first_num + random.randint(2,5)) * second_num

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
