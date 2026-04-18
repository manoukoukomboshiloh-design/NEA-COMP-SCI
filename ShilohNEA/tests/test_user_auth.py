import os
import sqlite3
import sys
import tempfile
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.oop_quiz import User


class UserAuthTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'user_data.db')
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                '''
                CREATE TABLE userdata (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
                '''
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_signup_creates_distinct_user_ids(self):
        first_user = User.create_user('alice', 'password123', db_path=self.db_path)
        second_user = User.create_user('bob', 'secret456', db_path=self.db_path)

        self.assertIsNotNone(first_user)
        self.assertIsNotNone(second_user)
        self.assertNotEqual(first_user.user_id, second_user.user_id)
        self.assertEqual(first_user.username, 'alice')
        self.assertEqual(second_user.username, 'bob')

    def test_authenticate_uses_created_credentials(self):
        created_user = User.create_user('charlie', 'pw12345', db_path=self.db_path)
        logged_in_user = User.authenticate('charlie', 'pw12345', db_path=self.db_path)

        self.assertIsNotNone(created_user)
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(created_user.user_id, logged_in_user.user_id)


if __name__ == '__main__':
    unittest.main()
