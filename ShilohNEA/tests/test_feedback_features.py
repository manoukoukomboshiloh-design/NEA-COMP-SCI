import json
import os
import sqlite3
import sys
import tempfile
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.mark_queries import get_pending_mark_queries, submit_mark_query
from quiz.display.question_bank import save_user_question


class FeedbackFeatureTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'user_data.db')
        self.json_path = os.path.join(self.temp_dir.name, 'user_questions.json')

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
            con.execute(
                "INSERT INTO userdata (username, password) VALUES (?, ?)",
                ('alice', 'hashed')
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_submit_mark_query_stores_pending_request(self):
        query_id = submit_mark_query(
            user_id=1,
            username='alice',
            topic='Waves',
            question_text='What is meant by coherent sources?',
            expected_answer='Same frequency and constant phase difference.',
            user_answer='same frequency and in phase',
            reason='This should still get the mark',
            db_path=self.db_path,
        )

        self.assertIsInstance(query_id, int)
        pending = get_pending_mark_queries(db_path=self.db_path)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]['status'], 'pending')
        self.assertEqual(pending[0]['username'], 'alice')

    def test_save_user_question_writes_to_json_file(self):
        save_user_question(
            topic='Mechanics',
            question='What is impulse?',
            answer='Impulse is the change in momentum.',
            json_path=self.json_path,
        )

        with open(self.json_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)

        self.assertIn('Mechanics', data['topics'])
        self.assertEqual(data['topics']['Mechanics'][0]['question'], 'What is impulse?')


if __name__ == '__main__':
    unittest.main()
