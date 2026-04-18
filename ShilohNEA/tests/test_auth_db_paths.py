import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from login.server.server import DB_PATH as SERVER_DB_PATH
from quiz.oop_quiz import DATABASE_PATH as QUIZ_DB_PATH


class AuthDatabasePathTests(unittest.TestCase):
    def test_login_server_uses_same_database_as_quiz_system(self):
        self.assertEqual(os.path.abspath(SERVER_DB_PATH), os.path.abspath(QUIZ_DB_PATH))


if __name__ == '__main__':
    unittest.main()
