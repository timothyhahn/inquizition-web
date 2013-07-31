CREATE TABLE question (
        id INTEGER NOT NULL, 
        correct_answer VARCHAR(120), 
        other_answer1 VARCHAR(120), 
        other_answer2 VARCHAR(120), 
        other_answer3 VARCHAR(120), 
        PRIMARY KEY (id)
);
CREATE TABLE quiz (
        id INTEGER NOT NULL, 
        name VARCHAR(50), 
        start_time DATETIME, 
        end_time DATETIME, 
        PRIMARY KEY (id)
);
CREATE TABLE response (
        id INTEGER NOT NULL, 
        answered BOOLEAN, 
        user_id INTEGER, 
        quiz_id INTEGER, 
        question_id INTEGER, 
        user_response VARCHAR(1), 
        correct_response VARCHAR(1), 
        time_elapsed DATETIME, 
        PRIMARY KEY (id), 
        CHECK (answered IN (0, 1)), 
        FOREIGN KEY(user_id) REFERENCES user (id), 
        FOREIGN KEY(quiz_id) REFERENCES quiz (id), 
        FOREIGN KEY(question_id) REFERENCES question (id)
);
CREATE TABLE result (
        id INTEGER NOT NULL, 
        user_id INTEGER, 
        score INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE user (
        id INTEGER NOT NULL, 
        name VARCHAR(80), 
        PRIMARY KEY (id)
);

