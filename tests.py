import os
import inquizition
import unittest
import tempfile

class InquizitionTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, inquizition.app.config['DATABASE'] = tempfile.mkstemp()
        inquizition.app.config['TESTING'] = True
        self.app = inquizition.app.test_client()
        inquizition.database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(inquizition.app.config['DATABASE'])


    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' not in rv.data


if __name__ == '__main__':
    unittest.main()
