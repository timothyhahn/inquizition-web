import os
from flask.ext.sqlalchemy import SQLAlchemy
import unittest
import tempfile
from flask import json
import inquizition


class InquizitionTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, inquizition.app.config['DATABASE'] = tempfile.mkstemp()
        inquizition.app.db = SQLAlchemy(inquizition.app)
        inquizition.app.config['TESTING'] = True
        inquizition.database.init_db()
        inquizition.helpers.gen_dummy_data()
        self.app = inquizition.app.test_client()
        self.app.post('/login', data=dict(username='tester'))

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(inquizition.app.config['DATABASE'])
        os.environ['TESTING'] = ''

    def test_static_redirect(self):
        rv = self.app.get('/')
        assert "You should be redirected" in rv.data
        assert "app/index.html" in rv.data

    def sampleQuiz(self):
        quiz_dict = dict()
        quiz_dict['quiz_name'] = 'QUIZ NAME'
        quiz_dict['seconds'] = 30
        return quiz_dict

    def test_create_quiz(self):
        rv = self.app.post('/quiz/create', data=self.sampleQuiz(), follow_redirects=True)
        assert 'CREATED' in rv.data
        rv = self.app.get('/quiz')
        data = json.loads(rv.data)
        assert self.sampleQuiz()['quiz_name'] in rv.data


if __name__ == '__main__':
    unittest.main()
